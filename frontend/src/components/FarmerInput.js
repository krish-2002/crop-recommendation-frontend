import React, { useState } from 'react';

const FarmerInput = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    soil_type: '',
    weather: '',
    region: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="farmer-input">
      <h2>Enter Farm Details</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="soil_type">Soil Type:</label>
          <select
            id="soil_type"
            name="soil_type"
            value={formData.soil_type}
            onChange={handleChange}
            required
          >
            <option value="">Select Soil Type</option>
            <option value="clay">Clay</option>
            <option value="sandy">Sandy</option>
            <option value="loamy">Loamy</option>
            <option value="silt">Silt</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="weather">Weather Condition:</label>
          <select
            id="weather"
            name="weather"
            value={formData.weather}
            onChange={handleChange}
            required
          >
            <option value="">Select Weather</option>
            <option value="sunny">Sunny</option>
            <option value="rainy">Rainy</option>
            <option value="cloudy">Cloudy</option>
            <option value="partly_cloudy">Partly Cloudy</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="region">Region:</label>
          <select
            id="region"
            name="region"
            value={formData.region}
            onChange={handleChange}
            required
          >
            <option value="">Select Region</option>
            <option value="north">North</option>
            <option value="south">South</option>
            <option value="east">East</option>
            <option value="west">West</option>
            <option value="central">Central</option>
          </select>
        </div>

        <button type="submit" className="submit-button">
          Get Crop Recommendation
        </button>
      </form>

      <style jsx>{`
        .farmer-input {
          max-width: 500px;
          margin: 20px auto;
          padding: 20px;
          background-color: white;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .form-group {
          margin-bottom: 20px;
        }

        label {
          display: block;
          margin-bottom: 5px;
          font-weight: bold;
        }

        select {
          width: 100%;
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 16px;
        }

        .submit-button {
          width: 100%;
          padding: 10px;
          background-color: #4CAF50;
          color: white;
          border: none;
          border-radius: 4px;
          font-size: 16px;
          cursor: pointer;
          transition: background-color 0.3s;
        }

        .submit-button:hover {
          background-color: #45a049;
        }
      `}</style>
    </div>
  );
};

export default FarmerInput; 