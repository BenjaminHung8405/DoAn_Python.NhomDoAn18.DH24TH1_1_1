import psycopg2
from psycopg2 import pool
from Database.config import DATABASE_CONFIG


class DatabaseConnection:
    """Singleton Database Connection Pool"""
    _instance = None
    _connection_pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            try:
                cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    1, 20,
                    DATABASE_CONFIG['connection_string']
                )
                print("✓ Database connection pool created successfully")
            except Exception as e:
                print(f"✗ Error creating connection pool: {e}")
                cls._connection_pool = None
        return cls._instance

    def get_connection(self):
        """Get a connection from the pool"""
        if self._connection_pool:
            return self._connection_pool.getconn()
        return None

    def return_connection(self, connection):
        """Return connection to the pool"""
        if self._connection_pool and connection:
            self._connection_pool.putconn(connection)

    def close_all_connections(self):
        """Close all connections in the pool"""
        if self._connection_pool:
            self._connection_pool.closeall()


def execute_query(query, params=None, fetch=True):
    """
    Execute a database query
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch: Whether to fetch results (True for SELECT, False for INSERT/UPDATE/DELETE)
    
    Returns:
        List of tuples (if fetch=True) or None
    """
    db = DatabaseConnection()
    connection = db.get_connection()
    
    if not connection:
        print("✗ Failed to get database connection")
        return None if fetch else False
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            db.return_connection(connection)
            return result
        else:
            connection.commit()
            cursor.close()
            db.return_connection(connection)
            return True
            
    except Exception as e:
        print(f"✗ Database error: {e}")
        connection.rollback()
        db.return_connection(connection)
        return None if fetch else False