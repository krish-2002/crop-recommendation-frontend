import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import FarmerInput from './FarmerInput';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const [sensorData, setSensorData] = useState([]);
  const [currentPrediction, setCurrentPrediction] = useState(null);
  const [systemStatus, setSystemStatus] = useState(null);
  const [showPrediction, setShowPrediction] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/sensor-data');
        const data = await response.json();
        setSensorData(data);
      } catch (error) {
        console.error('Error fetching sensor data:', error);
      }
    };

    const fetchStatus = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/system-status');
        const data = await response.json();
        setSystemStatus(data);
      } catch (error) {
        console.error('Error fetching system status:', error);
      }
    };

    fetchData();
    fetchStatus();
    const interval = setInterval(() => {
      fetchData();
      fetchStatus();
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const handleFarmerInput = async (formData) => {
    try {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      setCurrentPrediction(data);
      setShowPrediction(true);
    } catch (error) {
      console.error('Error getting prediction:', error);
    }
  };

  const chartData = {
    labels: sensorData.map(data => new Date(data.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: 'Temperature (°C)',
        data: sensorData.map(data => data.temperature),
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1,
      },
      {
        label: 'Humidity (%)',
        data: sensorData.map(data => data.humidity),
        borderColor: 'rgb(53, 162, 235)',
        tension: 0.1,
      },
      {
        label: 'Soil Moisture',
        data: sensorData.map(data => data.moisture),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
      {
        label: 'pH Level',
        data: sensorData.map(data => data.ph),
        borderColor: 'rgb(153, 102, 255)',
        tension: 0.1,
      },
    ],
  };

  return (
    <div className="dashboard">
      <h1>Crop Recommendation System Dashboard</h1>
      
      <div className="status-section">
        <h2>System Status</h2>
        {systemStatus && (
          <div className={`status-card ${systemStatus.status}`}>
            <p>Status: {systemStatus.status}</p>
            <p>Message: {systemStatus.message}</p>
            <p>Last Updated: {new Date(systemStatus.timestamp).toLocaleString()}</p>
          </div>
        )}
      </div>

      <div className="input-section">
        <FarmerInput onSubmit={handleFarmerInput} />
      </div>

      {showPrediction && currentPrediction && (
        <div className="prediction-section">
          <h2>Current Prediction</h2>
          <div className="prediction-card">
            <h3>Recommended Crop: {currentPrediction.prediction}</h3>
            <p>Confidence: {(currentPrediction.confidence * 100).toFixed(2)}%</p>
            <div className="prediction-details">
              <p>Based on:</p>
              <ul>
                <li>Soil Type: {currentPrediction.soil_type}</li>
                <li>Weather: {currentPrediction.weather}</li>
                <li>Region: {currentPrediction.region}</li>
                <li>Temperature: {currentPrediction.temperature}°C</li>
                <li>Humidity: {currentPrediction.humidity}%</li>
                <li>Soil Moisture: {currentPrediction.moisture}</li>
                <li>pH Level: {currentPrediction.ph}</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      <div className="charts-section">
        <h2>Sensor Data History</h2>
        <div className="chart-container">
          <Line data={chartData} options={{
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Sensor Data Over Time',
              },
            },
          }} />
        </div>
      </div>

      <style jsx>{`
        .dashboard {
          padding: 20px;
          max-width: 1200px;
          margin: 0 auto;
        }

        .status-section, .prediction-section, .charts-section, .input-section {
          margin-bottom: 30px;
        }

        .status-card {
          padding: 15px;
          border-radius: 8px;
          background-color: #f5f5f5;
        }

        .status-card.online {
          background-color: #e6ffe6;
        }

        .status-card.offline {
          background-color: #ffe6e6;
        }

        .status-card.error {
          background-color: #fff3e6;
        }

        .prediction-card {
          padding: 20px;
          border-radius: 8px;
          background-color: #f0f8ff;
          text-align: center;
        }

        .prediction-details {
          text-align: left;
          margin-top: 20px;
          padding: 15px;
          background-color: #f8f9fa;
          border-radius: 4px;
        }

        .prediction-details ul {
          list-style-type: none;
          padding: 0;
        }

        .prediction-details li {
          margin: 5px 0;
        }

        .chart-container {
          background-color: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
      `}</style>
    </div>
  );
};

export default Dashboard; 