"""Create minimal schema required by the app (idempotent).

Run this after configuring `DATABASE_URL` in `.env`.
Usage: cd to project root, then run: python -m Database.init_schema
"""
import sys
import os
# ensure we can import Gói Database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Database.config import get_connection, release_connection

SQL = [
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        display_name VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        password_hash VARCHAR(255),
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


def create_schema():
    conn = None
    try:
        conn = get_connection()
        if not conn:
            print('No DB connection available. Configure DATABASE_URL in .env')
            return False
        cur = conn.cursor()
        for s in SQL:
            cur.execute(s)
        conn.commit()
        print('Schema created/verified successfully')
        return True
    except Exception as e:
        print('Error creating schema:', e)
        return False
    finally:
        if conn:
            release_connection(conn)


if __name__ == '__main__':
    create_schema()
