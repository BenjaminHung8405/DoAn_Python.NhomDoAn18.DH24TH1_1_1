#!/usr/bin/env python3
"""
Database connection test script
Verifies that DATABASE_URL is correctly configured in .env
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connection"""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url or database_url == 'postgresql://user:password@host/database':
        print("Error: DATABASE_URL not configured in .env file")
        print("Please create .env file with:")
        print("  DATABASE_URL=postgresql://user:password@host:port/database")
        print("\nExample from Neon:")
        print("  DATABASE_URL=postgresql://user:password@ep-xxxx.region.neon.tech/dbname?sslmode=require")
        sys.exit(1)
    
    # Import after loading env
    try:
        import psycopg2
    except ImportError:
        print("Error: psycopg2 not installed")
        print("Run: pip install psycopg2-binary")
        sys.exit(1)
    
    print("Testing database connection...")
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        print("✓ Database connection successful!")
        print("\nNote: Schema setup must be done manually in Neon console or using migrations.")
        print("This app uses remote Neon PostgreSQL database only.")
        
        return True
        
    except psycopg2.Error as e:
        print(f"✗ Database connection failed: {e}")
        print("\nPlease check your DATABASE_URL in .env file")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("Amplify Music Player - Database Connection Test")
    print("="*60)
    print()
    
    success = test_database_connection()
    sys.exit(0 if success else 1)
