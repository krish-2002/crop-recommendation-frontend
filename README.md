# Smart Crop Recommendation System

This system uses various sensors to collect soil and environmental data to recommend the best crop for farming.

## Hardware Requirements
- ESP32 Development Board
- DHT11 Temperature and Humidity Sensor
- Soil Moisture Sensor
- NPK Sensor (Nitrogen, Phosphorus, Potassium)
- Jumper Wires
- Breadboard

## Software Requirements
- Python 3.8+
- Arduino IDE
- Required Python packages (listed in requirements.txt)
- Required Arduino libraries (listed in esp32/README.md)

## System Components

1. **ESP32 Sensor Node**
   - DHT11 Temperature and Humidity Sensor
   - Soil Moisture Sensor
   - NPK Sensor
   - MQTT Communication

2. **Backend Server**
   - Flask API
   - SQLite Database
   - MQTT Client
   - Crop Prediction Model

3. **Web Dashboard**
   - Real-time Sensor Data Display
   - Farmer Input Form
   - Crop Recommendations
   - Historical Data Visualization

## Setup Instructions

### 1. ESP32 Setup

1. Install required libraries in Arduino IDE:
   - WiFi
   - PubSubClient
   - DHT
   - ArduinoJson

2. Update the following in `esp32/sensor_node.ino`:
   - WiFi credentials
   - MQTT broker details
   - Sensor pins

3. Upload the code to ESP32

### 2. Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the backend directory with:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the backend server:
   ```bash
   flask run
   ```

### 3. Frontend Setup

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## API Endpoints

1. `GET /api/sensor-data`
   - Returns latest sensor readings

2. `POST /api/predict`
   - Accepts farmer input and returns crop recommendation
   - Required fields: soil_type, weather, region

3. `GET /api/system-status`
   - Returns current system status and sensor readings

## Project Structure

```
Crop_Recommendation_Integration/
├── esp32/
│   └── sensor_node.ino
├── backend/
│   ├── app.py
│   ├── models.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── components/
│   │       ├── Dashboard.js
│   │       └── FarmerInput.js
│   └── package.json
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 