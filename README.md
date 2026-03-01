# Zephyr: RFID Payment System

Zephyr is a comprehensive RFID-based payment system designed for seamless and real-time transactions. The project integrates a hardware RFID reader, a backend server, and a frontend web application to create a complete and interactive payment experience.

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Hardware Setup](#hardware-setup)
  - [Backend Setup](#backend-setup)
  - [Frontend Access](#frontend-access)
- [Usage](#usage)
- [Technologies Used](#technologies-used)

## Features

- **Real-time Card Detection:** Instantly detects RFID cards and communicates their UIDs to the backend.
- **Seamless Transactions:** Supports both payment and top-up functionalities through a user-friendly web interface.
- **Live Dashboard:** A sophisticated frontend that displays real-time updates of card information, balance, and transaction history.
- **Centralized Logic:** A robust backend server that manages all business logic, user data, and communication between components.
- **Persistent Data:** Utilizes a SQLite database to store user card information and transaction records.

## System Architecture

The Zephyr payment system is composed of three main components that work in concert:

### 1. Hardware (ESP8266 RFID Reader)

The hardware component is responsible for the physical interaction with the RFID cards.

- **Device:** ESP8266
- **RFID Module:** MFRC522
- **Core Functionality:**
    - Establishes a connection to a Wi-Fi network and an MQTT broker.
    - Scans for RFID cards and publishes the card's UID to a designated MQTT topic.
    - Subscribes to MQTT topics to receive real-time updates for payments and top-ups.
    - Capable of writing updated balance information back to the RFID card.

The source code for the hardware is located in the `ESP_RFID/ESP_RFID.ino` file.

### 2. Backend (Flask Server)

The backend is the heart of the system, orchestrating all operations and data flow.

- **Framework:** Flask
- **Database:** SQLite
- **Real-time Communication:** Employs MQTT for hardware communication and Socket.IO for frontend updates.
- **Core Functionality:**
    - Manages user card data and balances within a SQLite database.
    - Processes all payment and top-up requests.
    - Acts as a bridge between the RFID reader and the web application.
    - Pushes live updates to the frontend dashboard.

The backend application logic is defined in `backend/app.py`.

### 3. Frontend (Web Application)

The frontend provides a rich and interactive user interface for the payment system.

- **Styling and Frameworks:** Built with Tailwind CSS and leverages Socket.IO for real-time data synchronization.
- **Core Functionality:**
    - Presents a "museum-themed" dashboard for a unique user experience.
    - Facilitates topping up RFID cards and making payments for a curated list of products.
    - Dynamically updates to show the current card UID, balance, and a ledger of transactions.

The frontend is a single-page application, with its structure and code in `backend/templates/dashboard.html`.

## Getting Started

To get the Zephyr payment system up and running, follow the setup instructions for each component.

### Prerequisites

- Arduino IDE for the hardware setup.
- Python 3.x and `pip` for the backend server.
- A modern web browser for the frontend application.

### Hardware Setup

1.  Launch the Arduino IDE and open the `ESP_RFID/ESP_RFID.ino` file.
2.  Install the necessary libraries from the Arduino Library Manager: `ESP8266WiFi`, `PubSubClient`, `MFRC522`, and `ArduinoJson`.
3.  Modify the sketch to include your Wi-Fi credentials (`WIFI_SSID` and `WIFI_PASS`) and your `TEAM_ID`.
4.  Connect your ESP8266 and upload the sketch.

### Backend Setup

1.  Open your terminal and navigate to the `Payment` directory.
2.  Install the required Python packages by running:
    ```bash
    pip install Flask Flask-SocketIO Flask-Cors Flask-SQLAlchemy paho-mqtt
    ```
3.  Start the backend server with the following command:
    ```bash
    python backend/app.py
    ```

### Frontend Access

1.  Once the backend server is running, open your web browser.
2.  Navigate to `http://157.173.101.159:9277` to access the Zephyr dashboard.

## Usage

- **Card Scanning:** Simply bring an RFID card near the MFRC522 reader. The card's UID and current balance will appear on the dashboard.
- **Topping Up:** Use the "Authorize Deposit" section to add funds to the scanned card.
- **Making a Payment:** Select a product from the gallery, and click "Acquire Asset" to complete the purchase. The transaction will be reflected in the ledger.

## Technologies Used

- **Hardware:** ESP8266, MFRC522 RFID Module
- **Backend:** Python, Flask, Flask-SocketIO, Flask-SQLAlchemy
- **Frontend:** HTML, Tailwind CSS, JavaScript, Socket.IO
- **Communication:** MQTT, WebSockets
- **Database:** SQLite
