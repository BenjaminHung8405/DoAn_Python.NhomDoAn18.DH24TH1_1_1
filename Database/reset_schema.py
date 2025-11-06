"""Drop all tables and recreate schema from scratch.

WARNING: This will DELETE ALL DATA in the database!

Usage: python -m Database.reset_schema
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Database.config import get_connection, release_connection

DROP_SQL = [
    "DROP TABLE IF EXISTS user_likes CASCADE",
    "DROP TABLE IF EXISTS albums_tracks CASCADE",
    "DROP TABLE IF EXISTS albums CASCADE",
    "DROP TABLE IF EXISTS tracks CASCADE",
    "DROP TABLE IF EXISTS languages CASCADE",
    "DROP TABLE IF EXISTS genres CASCADE",
    "DROP TABLE IF EXISTS artists CASCADE",
    "DROP TABLE IF EXISTS users CASCADE",
]

CREATE_SQL = [
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        display_name VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        phone_number VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS artists (
        artist_id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE,
        image_url TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS genres (
        genre_id SERIAL PRIMARY KEY,
        genre_name VARCHAR(100) UNIQUE,
        genre_image TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS languages (
        language_id SERIAL PRIMARY KEY,
        language_name VARCHAR(100) UNIQUE,
        language_image TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tracks (
        track_id SERIAL PRIMARY KEY,
        title VARCHAR(255) UNIQUE,
        artist VARCHAR(255),
        genre VARCHAR(100),
        location TEXT,
        language VARCHAR(100),
        like_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS albums (
        album_id SERIAL PRIMARY KEY,
        album_title VARCHAR(255) UNIQUE,
        artist VARCHAR(255)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS albums_tracks (
        album_id INTEGER REFERENCES albums(album_id) ON DELETE CASCADE,
        track_id INTEGER REFERENCES tracks(track_id) ON DELETE CASCADE,
        PRIMARY KEY (album_id, track_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS user_likes (
        user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
        track_id INTEGER REFERENCES tracks(track_id) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, track_id)
    )
    """,
]


def reset_schema():
    conn = None
    try:
        conn = get_connection()
        if not conn:
            print('❌ No DB connection available. Configure DATABASE_URL in .env')
            return False
        
        cur = conn.cursor()
        
        print('🗑️  Dropping all existing tables...')
        for sql in DROP_SQL:
            cur.execute(sql)
            print(f'   ✓ {sql.split()[4]}')
        
        print('\n📊 Creating new schema...')
        for sql in CREATE_SQL:
            cur.execute(sql)
            table_name = sql.strip().split()[5]
            print(f'   ✓ {table_name}')
        
        conn.commit()
        print('\n✅ Schema reset successfully!')
        return True
    except Exception as e:
        print(f'❌ Error resetting schema: {e}')
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            release_connection(conn)


if __name__ == '__main__':
    print('⚠️  WARNING: This will DELETE ALL DATA in the database!')
    response = input('Are you sure you want to continue? (yes/no): ')
    if response.lower() == 'yes':
        reset_schema()
    else:
        print('Cancelled.')
