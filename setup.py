#!/usr/bin/env python3
"""
Setup script for Amplify Music Player - PostgreSQL Version
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required packages"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Error installing dependencies")
        sys.exit(1)

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("\nCreating .env file from template...")
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✓ .env file created")
            print("⚠ Please edit .env file and add your DATABASE_URL")
        else:
            print("✗ .env.example not found")
    else:
        print("\n✓ .env file already exists")

def check_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        from Database.config import get_connection, release_connection
        conn = get_connection()
        if conn:
            print("✓ Database connection successful")
            release_connection(conn)
            return True
        else:
            print("✗ Could not connect to database")
            print("  Please check your DATABASE_URL in .env file")
            return False
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("  Please check your DATABASE_URL in .env file")
        return False

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    dirs = ['images', 'fonts', 'Music']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✓ Directories created")

def main():
    print("=" * 60)
    print("Amplify Music Player - Setup")
    print("=" * 60)
    
    check_python_version()
    create_directories()
    install_dependencies()
    create_env_file()
    
    print("\n" + "=" * 60)
    print("Setup completed!")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Edit .env file and add your Neon DATABASE_URL")
    print("2. Ensure your Neon database schema is set up (create tables)")
    print("3. Copy images from Amplify-master/images/ to images/")
    print("4. Run: python main.py")
    
    print("\nTesting database connection...")
    if check_database_connection():
        print("\n✓ All set! You can now run: python main.py")
    else:
        print("\n⚠ Please configure database before running the app")

if __name__ == "__main__":
    main()
