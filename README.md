💳 Tap-To-Pay Smart Payment System


🔒 Secure RFID-Based Cashless Payment System using ESP8266 + MQTT + Backend Validation

🌐 Frontend Application

👉 Live Frontend Dashboard:
🔗 http://157.173.101.159:9277/

The frontend dashboard allows:

Transaction monitoring

Wallet balance tracking

Payment history viewing

System analytics visualization

🏗 System Architecture
RFID Card
   ↓
ESP8266 IoT Device
   ↓
MQTT Broker Communication
   ↓
Backend API Validation
   ↓
Database Transaction Storage
   ↓
Web Dashboard Updates
✨ Features

✔ RFID Card Authentication
✔ Real-time Payment Processing
✔ Secure Wallet Balance Verification
✔ Transaction Ledger Recording
✔ Dashboard Monitoring System
✔ Safe Payment Update Mechanism

🧠 Technologies Used
Hardware

ESP8266 Microcontroller

RFID Reader Module

Buzzer Feedback System

Software

MQTT Communication Protocol

Backend API Service

Database Storage System

Web Frontend Dashboard

⚡ Installation
Clone Project
git clone https://github.com/utujesandrine456/Tap-To-Pay.git
Navigate Project
cd Tap-To-Pay
🔌 Hardware Connection
Component	ESP8266 Pin
RFID SDA	D2
RFID SCK	D5
RFID MOSI	D7
RFID MISO	D6
Buzzer	D1
💰 Payment Processing Flow
RFID Scan
   ↓
Send UID via MQTT
   ↓
Backend Validates Balance
   ↓
Update Wallet + Ledger
   ↓
Send Response to Device
🔐 Security Design

Backend controlled authorization

Ledger-based transaction auditing

Safe wallet update logic
