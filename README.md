🚀 Zephyr: RFID Smart Payment System
🌟 Overview

Zephyr is a smart RFID-based payment system designed for fast, secure, and real-time transactions. The platform integrates hardware sensing, backend processing, and a modern web dashboard to create a seamless payment experience.

Users can scan RFID cards, check balances instantly, perform top-ups, and purchase products from an interactive dashboard.

✨ Features

✅ Real-time RFID card detection
✅ Instant balance and transaction updates
✅ Secure payment and top-up system
✅ Live dashboard synchronization
✅ Centralized backend business logic
✅ Persistent transaction storage using SQLite

🏗 System Architecture
🧩 Hardware Layer (ESP8266 + RFID)

Device: ESP8266

RFID Module: MFRC522

Functions:

Connects to WiFi and MQTT broker

Reads RFID card UID

Sends transaction data to backend

Writes updated balance to cards

Code located in:

ESP_RFID/ESP_RFID.ino
⚙ Backend Layer (Flask Server)

Framework: Flask

Database: SQLite

Communication:

MQTT → Hardware communication

Socket.IO → Frontend real-time updates

Responsibilities:

Manage users and balances

Process payments and deposits

Broadcast dashboard updates

Main file:

backend/app.py
🎨 Frontend Layer

Technologies:

Tailwind CSS

Socket.IO

JavaScript

Features:

Museum-themed interactive dashboard

Product purchasing system

Live transaction ledger

Real-time card scanning display

Dashboard:

http://157.173.101.159:9224/topup
🚀 Getting Started
Prerequisites

Arduino IDE

Python 3.x

Modern web browser

Hardware Setup

Open ESP_RFID/ESP_RFID.ino in Arduino IDE

Install libraries:

ESP8266WiFi  
PubSubClient  
MFRC522  
ArduinoJson

Configure WiFi credentials and TEAM_ID

Upload code to ESP8266

Backend Setup
cd Payment
pip install Flask Flask-SocketIO Flask-Cors Flask-SQLAlchemy paho-mqtt
python backend/app.py
💳 Usage
Card Scanning

Place RFID card near reader → Dashboard updates instantly.

Top Up Funds

Use deposit authorization panel to add funds.

Make Payments

Select product → Click Acquire Asset → Transaction is recorded.

🛠 Technologies Used
Hardware

ESP8266

MFRC522 RFID

Backend

Python

Flask

SQLite

MQTT

WebSockets

Frontend

HTML

Tailwind CSS

JavaScript
