from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion # Added for v2 compatibility
import json
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'zephyr_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# --- MODELS ---
class UserCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), unique=True, nullable=False)
    balance = db.Column(db.Integer, default=0)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# --- CONFIGURATION (UPDATED) ---
TEAM_ID = "team_zephyr"
MQTT_BROKER = "broker.benax.rw"
TOPIC_STATUS = f"rfid/{TEAM_ID}/card/status"
TOPIC_PAY = f"rfid/{TEAM_ID}/card/pay"
TOPIC_TOPUP = f"rfid/{TEAM_ID}/card/topup"

# --- MQTT LOGIC ---
def on_connect(client, userdata, flags, rc):
    print(f"[*] MQTT Connected to: {MQTT_BROKER}")
    client.subscribe(TOPIC_STATUS)

def on_message(client, userdata, msg):
    with app.app_context():
        try:
            payload = json.loads(msg.payload.decode())
            uid = str(payload.get('uid')).upper().strip()
            if uid:
                card = UserCard.query.filter_by(uid=uid).first()
                if not card:
                    card = UserCard(uid=uid, balance=0)
                    db.session.add(card)
                card.last_seen = datetime.utcnow()
                db.session.commit()
                socketio.emit('update_ui', {
                    "uid": uid,
                    "balance": card.balance,
                    "type": "SCAN",
                    "time": datetime.now().strftime("%H:%M:%S")
                })
        except Exception as e:
            print(f"[!] MQTT Error: {e}")

# Updated with CallbackAPIVersion to fix deprecation warning
mqtt_client = mqtt.Client(CallbackAPIVersion.VERSION1)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()
except Exception as e:
    print(f"MQTT Connection Failed: {e}")

# --- ROUTES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/agent', methods=['GET'])
def agent_login():
    return render_template('agent_login.html')

@app.route('/login/sales', methods=['GET'])
def sales_login():
    return render_template('sales_login.html')

@app.route('/login/agent', methods=['POST'])
def login_agent():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'agent' and password == 'agentpass':
        session['role'] = 'agent'
        return redirect(url_for('topup_dashboard'))
    else:
        return redirect(url_for('agent_login'))

@app.route('/login/sales', methods=['POST'])
def login_sales():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'sales' and password == 'salespass':
        session['role'] = 'sales'
        return redirect(url_for('payment_dashboard'))
    else:
        return redirect(url_for('sales_login'))

@app.route('/topup-dashboard')
def topup_dashboard():
    if session.get('role') != 'agent':
        return redirect(url_for('agent_login'))
    return render_template('dashboard.html')

@app.route('/payment-dashboard')
def payment_dashboard():
    if session.get('role') != 'sales':
        return redirect(url_for('sales_login'))
    return render_template('dashboard.html')

@app.route('/consolidated-dashboard')
def consolidated_dashboard():
    if session.get('role') not in ('agent', 'sales'):
        return redirect(url_for('login'))
    users = UserCard.query.order_by(UserCard.last_seen.desc()).all()
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    topups = [tx for tx in transactions if tx.type == "TOP-UP"]
    total_balances = sum(user.balance for user in users)
    total_topups = sum(tx.amount for tx in topups)
    total_payments = sum(tx.amount for tx in transactions if tx.type == "PAYMENT")
    return render_template(
        'consolidated_dashboard.html',
        users=users,
        transactions=transactions,
        topups=topups,
        total_balances=total_balances,
        total_topups=total_topups,
        total_payments=total_payments
    )

@app.route('/admin')
def admin():
    users = UserCard.query.all()
    transactions = Transaction.query.all()
    return render_template('admin.html', users=users, transactions=transactions)

@app.route('/pay', methods=['POST'])
def pay():
    data = request.json
    uid = str(data.get('uid')).upper().strip()
    amount = int(data.get('amount', 0))
    product_name = str(data.get('product_name', 'General Purchase')).strip() or 'General Purchase'
    try:
        quantity = max(int(data.get('quantity', 1)), 1)
    except (TypeError, ValueError):
        quantity = 1
    card = UserCard.query.filter_by(uid=uid).first()
    if not card: return jsonify({"error": "Card not registered"}), 404
    if card.balance >= amount:
        card.balance -= amount
        tx = Transaction(uid=uid, amount=amount, type="PAYMENT")
        db.session.add(tx)
        db.session.commit()
        mqtt_client.publish(TOPIC_PAY, json.dumps({"uid": uid, "new_balance": card.balance}))
        tx_time = tx.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        res_data = {"uid": uid, "balance": card.balance, "amount": amount, "type": "PAYMENT", "time": datetime.now().strftime("%H:%M:%S"), "transaction_id": tx.id}
        socketio.emit('update_ui', res_data)
        receipt = {
            "transaction_id": tx.id,
            "uid": uid,
            "item": product_name,
            "quantity": quantity,
            "amount": amount,
            "remaining_balance": card.balance,
            "timestamp": tx_time
        }
        return jsonify({"status": "success", "new_balance": card.balance, "receipt": receipt}), 200
    return jsonify({"error": "Insufficient Funds"}), 400

@app.route('/topup', methods=['POST'])
def topup():
    data = request.json
    uid = str(data.get('uid')).upper().strip()
    amount = int(data.get('amount', 0))
    if not uid or uid == "--- --- ---": return jsonify({"error": "Scan card first"}), 400
    card = UserCard.query.filter_by(uid=uid).first()
    if not card:
        card = UserCard(uid=uid, balance=0)
        db.session.add(card)
    card.balance += amount
    db.session.add(Transaction(uid=uid, amount=amount, type="TOP-UP"))
    db.session.commit()
    mqtt_client.publish(TOPIC_TOPUP, json.dumps({"uid": uid, "new_balance": card.balance}))
    res_data = {"uid": uid, "balance": card.balance, "amount": amount, "type": "TOP-UP", "time": datetime.now().strftime("%H:%M:%S")}
    socketio.emit('update_ui', res_data)
    return jsonify({"status": "success", "new_balance": card.balance}), 200

if __name__ == '__main__':
    # UPDATED PORT
    socketio.run(app, host='0.0.0.0', port=9277, debug=True)
