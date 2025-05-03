import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

def validate_dataset(file_path):
    try:
        # Read the dataset
        print(f"Reading dataset from: {file_path}")
        df = pd.read_csv(file_path)
        
        # Display basic information
        print("\nDataset Information:")
        print(f"Number of samples: {len(df)}")
        print(f"Number of features: {len(df.columns)}")
        print("\nColumn names:")
        for col in df.columns:
            print(f"- {col}")
        
        # Check for required columns
        required_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'moisture', 'rainfall', 'label']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print("\n❌ Missing required columns:")
            for col in missing_columns:
                print(f"- {col}")
            return False
        
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.any():
            print("\n❌ Found missing values:")
            print(missing_values[missing_values > 0])
            return False
        
        # Check data types
        print("\nData types:")
        print(df.dtypes)
        
        # Check value ranges
        print("\nValue ranges:")
        for col in df.columns:
            if col != 'label':
                print(f"{col}: {df[col].min():.2f} to {df[col].max():.2f}")
        
        # Check unique crop labels
        print("\nUnique crop labels:")
        print(df['label'].unique())
        
        # Basic statistics
        print("\nBasic statistics:")
        print(df.describe())
        
        # Check for outliers
        print("\nChecking for outliers...")
        for col in df.columns:
            if col != 'label':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)][col]
                if len(outliers) > 0:
                    print(f"Found {len(outliers)} outliers in {col}")
        
        print("\n✅ Dataset validation completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error validating dataset: {str(e)}")
        return False

def prepare_dataset(file_path):
    try:
        # Read the dataset
        df = pd.read_csv(file_path)
        
        # Handle missing values if any
        df = df.fillna(df.mean())
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Save processed dataset
        processed_path = os.path.join(os.path.dirname(file_path), 'processed_crop_recommendation.csv')
        df.to_csv(processed_path, index=False)
        print(f"\n✅ Processed dataset saved to: {processed_path}")
        
        return processed_path
        
    except Exception as e:
        print(f"\n❌ Error preparing dataset: {str(e)}")
        return None

if __name__ == "__main__":
    # Path to your dataset
    dataset_path = os.path.join('data', 'crop_recommendation.csv')
    
    # Validate dataset
    if validate_dataset(dataset_path):
        # Prepare dataset
        processed_path = prepare_dataset(dataset_path)
        if processed_path:
            print("\nDataset is ready to use!")
    else:
        print("\nPlease fix the issues in your dataset and try again.") 