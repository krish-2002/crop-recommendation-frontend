// Test script to verify frontend-backend connection
const testBackendConnection = async () => {
    try {
        // Test sensor data endpoint
        const sensorResponse = await fetch('http://localhost:5000/api/sensor-data');
        if (!sensorResponse.ok) {
            throw new Error(`Sensor data endpoint failed: ${sensorResponse.statusText}`);
        }
        console.log('✅ Sensor data endpoint working');

        // Test system status endpoint
        const statusResponse = await fetch('http://localhost:5000/api/system-status');
        if (!statusResponse.ok) {
            throw new Error(`System status endpoint failed: ${statusResponse.statusText}`);
        }
        console.log('✅ System status endpoint working');

        // Test prediction endpoint
        const testData = {
            soil_type: 'clay',
            weather: 'sunny',
            region: 'north'
        };
        const predictionResponse = await fetch('http://localhost:5000/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData)
        });
        if (!predictionResponse.ok) {
            throw new Error(`Prediction endpoint failed: ${predictionResponse.statusText}`);
        }
        console.log('✅ Prediction endpoint working');

        console.log('\n✅ All backend endpoints are working correctly!');
    } catch (error) {
        console.error('❌ Error testing backend connection:', error.message);
        console.log('\nTroubleshooting steps:');
        console.log('1. Make sure the backend server is running (python app.py)');
        console.log('2. Check if the backend is running on port 5000');
        console.log('3. Verify CORS is enabled in the backend');
        console.log('4. Check if the database is properly initialized');
    }
};

// Run the test
testBackendConnection(); 