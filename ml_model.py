import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CropRecommendationModel:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_columns = [
            'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall',
            'soil_type', 'weather', 'region'
        ]
        self.categorical_columns = ['soil_type', 'weather', 'region']
        self.model_path = 'models/crop_model.joblib'
        self.encoders_path = 'models/label_encoders.joblib'
        
    def load_data(self, file_path):
        """Load and preprocess the dataset"""
        try:
            logger.info(f"Loading dataset from {file_path}")
            df = pd.read_csv(file_path)
            
            # Verify required columns
            required_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Add categorical columns if not present
            if 'soil_type' not in df.columns:
                df['soil_type'] = 'alluvial'  # Default soil type
            if 'weather' not in df.columns:
                df['weather'] = 'sunny'  # Default weather
            if 'region' not in df.columns:
                df['region'] = 'karnataka'  # Default region
                
            logger.info(f"Dataset loaded successfully with {len(df)} samples")
            return df
            
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise
            
    def preprocess_data(self, df):
        """Preprocess the data for training"""
        try:
            # Create label encoders for categorical variables
            for col in self.categorical_columns:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col])
            
            # Prepare features and target
            X = df[self.feature_columns]
            y = df['label']
            
            logger.info("Data preprocessing completed")
            return X, y
            
        except Exception as e:
            logger.error(f"Error preprocessing data: {str(e)}")
            raise
            
    def train(self, file_path):
        """Train the model"""
        try:
            # Load and preprocess data
            df = self.load_data(file_path)
            X, y = self.preprocess_data(df)
            
            # Initialize and train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.model.fit(X, y)
            
            # Save model and encoders
            os.makedirs('models', exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.label_encoders, self.encoders_path)
            
            logger.info("Model trained and saved successfully")
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise
            
    def load_model(self):
        """Load the trained model and encoders"""
        try:
            if not os.path.exists(self.model_path) or not os.path.exists(self.encoders_path):
                raise FileNotFoundError("Model files not found. Please train the model first.")
                
            self.model = joblib.load(self.model_path)
            self.label_encoders = joblib.load(self.encoders_path)
            logger.info("Model and encoders loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
            
    def predict(self, input_data):
        """Make predictions"""
        try:
            if self.model is None:
                self.load_model()
                
            # Prepare input data
            input_df = pd.DataFrame([input_data])
            
            # Transform categorical variables
            for col in self.categorical_columns:
                if col in input_df.columns:
                    input_df[col] = self.label_encoders[col].transform(input_df[col])
            
            # Make prediction
            prediction = self.model.predict(input_df)[0]
            probabilities = self.model.predict_proba(input_df)[0]
            confidence = max(probabilities)
            
            return {
                'crop': prediction,
                'confidence': float(confidence)
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise 