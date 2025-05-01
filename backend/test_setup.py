import os
import sys
from pathlib import Path

def check_dataset():
    print("\nChecking dataset...")
    dataset_path = Path('data/crop_recommendation.csv')
    if dataset_path.exists():
        print("✅ Dataset found at:", dataset_path)
        return True
    else:
        print("❌ Dataset not found at:", dataset_path)
        print("Please place your dataset at:", dataset_path.absolute())
        return False

def check_database():
    print("\nChecking database...")
    db_path = Path('crop_recommendation.db')
    if db_path.exists():
        print("✅ Database file exists")
        return True
    else:
        print("❌ Database file not found")
        print("Database will be created when you run the application")
        return True

def check_models():
    print("\nChecking ML models...")
    models_dir = Path('models')
    if models_dir.exists():
        print("✅ Models directory exists")
        return True
    else:
        print("❌ Models directory not found")
        print("Models directory will be created when you run the application")
        return True

def check_dependencies():
    print("\nChecking dependencies...")
    try:
        import flask
        import flask_cors
        import flask_sqlalchemy
        import paho.mqtt.client
        import numpy
        import pandas
        import sklearn
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print("❌ Missing package:", str(e))
        print("Please install required packages using: pip install -r requirements.txt")
        return False

def main():
    print("Starting system check...")
    
    # Check all components
    dataset_ok = check_dataset()
    database_ok = check_database()
    models_ok = check_models()
    dependencies_ok = check_dependencies()
    
    # Summary
    print("\nSystem Check Summary:")
    print("Dataset:", "✅" if dataset_ok else "❌")
    print("Database:", "✅" if database_ok else "❌")
    print("ML Models:", "✅" if models_ok else "❌")
    print("Dependencies:", "✅" if dependencies_ok else "❌")
    
    if all([dataset_ok, database_ok, models_ok, dependencies_ok]):
        print("\n✅ All components are ready!")
        print("\nTo start the system:")
        print("1. Run the backend server: python app.py")
        print("2. Start the frontend: cd ../frontend && npm start")
    else:
        print("\n❌ Some components need attention. Please fix the issues above.")

if __name__ == "__main__":
    main() 