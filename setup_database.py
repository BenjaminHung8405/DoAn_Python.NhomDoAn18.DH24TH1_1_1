#!/usr/bin/env python3
"""
Database setup script - Import schema and seed data
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Setup database schema and seed data"""
    
    # Import after loading env
    try:
        import psycopg2
    except ImportError:
        print("Error: psycopg2 not installed")
        print("Run: pip install psycopg2-binary")
        sys.exit(1)
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url or database_url == 'postgresql://user:password@host/database':
        print("Error: DATABASE_URL not configured in .env file")
        print("Please edit .env and add your Neon connection string")
        sys.exit(1)
    
    print("Connecting to database...")
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("✓ Connected successfully!")
        
        # Read and execute schema
        print("\nImporting schema...")
        with open('sql/schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            cursor.execute(schema_sql)
            conn.commit()
        print("✓ Schema imported successfully")
        
        # Ask if user wants to import seed data
        response = input("\nDo you want to import sample data? (y/n): ").strip().lower()
        
        if response == 'y':
            print("\nImporting seed data...")
            with open('sql/seed.sql', 'r', encoding='utf-8') as f:
                seed_sql = f.read()
                cursor.execute(seed_sql)
                conn.commit()
            print("✓ Seed data imported successfully")
        
        # Verify tables
        print("\nVerifying tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        print(f"\n✓ Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check sample data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tracks")
        track_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM artists")
        artist_count = cursor.fetchone()[0]
        
        print(f"\nDatabase Statistics:")
        print(f"  Users: {user_count}")
        print(f"  Tracks: {track_count}")
        print(f"  Artists: {artist_count}")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✓ Database setup completed successfully!")
        print("="*60)
        print("\nYou can now run: python main.py")
        
    except psycopg2.Error as e:
        print(f"\n✗ Database error: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\n✗ File not found: {e}")
        print("Make sure sql/schema.sql and sql/seed.sql exist")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("="*60)
    print("Amplify Music Player - Database Setup")
    print("="*60)
    print()
    
    setup_database()
