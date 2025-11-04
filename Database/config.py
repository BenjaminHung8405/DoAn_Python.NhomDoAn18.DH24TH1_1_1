import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection string from Neon
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@host/database')

# Tạo connection pool để quản lý kết nối
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1,  # minimum connections
        10,  # maximum connections
        DATABASE_URL
    )
    
    if connection_pool:
        print("Database connection pool created successfully")
except Exception as e:
    print(f"Error creating connection pool: {e}")
    print("Please check your DATABASE_URL in .env file")
    connection_pool = None


def get_connection():
    """Get a connection from the pool"""
    if connection_pool:
        return connection_pool.getconn()
    return None


def release_connection(conn):
    """Return a connection to the pool"""
    if connection_pool and conn:
        connection_pool.putconn(conn)

