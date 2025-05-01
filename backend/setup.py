import os
import sys
import subprocess
from pathlib import Path

def create_directories():
    print("\nCreating necessary directories...")
    directories = ['data', 'models']
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir()
            print(f"✅ Created directory: {dir_name}")
        else:
            print(f"✅ Directory already exists: {dir_name}")

def install_dependencies():
    print("\nInstalling required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        print("Please run: pip install -r requirements.txt manually")

def check_dataset():
    print("\nChecking dataset...")
    dataset_path = Path('data/crop_recommendation.csv')
    if not dataset_path.exists():
        print("❌ Dataset not found!")
        print("Please place your dataset at:", dataset_path.absolute())
        print("The dataset should be a CSV file with these columns:")
        print("- N (Nitrogen)")
        print("- P (Phosphorus)")
        print("- K (Potassium)")
        print("- temperature")
        print("- humidity")
        print("- ph")
        print("- rainfall")
        print("- label (crop name)")
        return False
    return True

def initialize_database():
    print("\nInitializing database...")
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        return False
    return True

def main():
    print("Starting setup...")
    
    # Create directories
    create_directories()
    
    # Install dependencies
    install_dependencies()
    
    # Check dataset
    dataset_ok = check_dataset()
    
    # Initialize database
    db_ok = initialize_database()
    
    # Summary
    print("\nSetup Summary:")
    print("Directories:", "✅")
    print("Dependencies:", "✅")
    print("Dataset:", "✅" if dataset_ok else "❌")
    print("Database:", "✅" if db_ok else "❌")
    
    if dataset_ok and db_ok:
        print("\n✅ Setup completed successfully!")
        print("\nTo start the system:")
        print("1. Run the backend server: python app.py")
        print("2. Start the frontend: cd ../frontend && npm start")
    else:
        print("\n❌ Setup completed with some issues.")
        print("Please fix the issues above before running the system.")

if __name__ == "__main__":
    main() 