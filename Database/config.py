import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
load_dotenv()

# Chuỗi kết nối PostgreSQL từ .env (Neon)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@host/database')

# Tạo connection pool để quản lý các kết nối DB
connection_pool = None
try:
	# Thêm chế độ SSL nếu không có trong DATABASE_URL
	db_url = DATABASE_URL
	if '?' not in db_url:
		db_url += '?sslmode=require'
	elif 'sslmode' not in db_url:
		db_url += '&sslmode=require'
	
	connection_pool = psycopg2.pool.SimpleConnectionPool(
		1,  # số kết nối tối thiểu
		10,  # số kết nối tối đa
		db_url,
		connect_timeout=10  # Thêm timeout để tránh treo
	)
	if connection_pool:
		print("✓ Database connection pool created successfully")
except Exception as e:
	print(f"⚠ Warning: Could not create DB connection pool: {e}")
	print("Application will run with limited functionality until DATABASE_URL is configured correctly.")
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


def test_connection():
	try:
		conn = get_connection()
		if conn:
			cur = conn.cursor()
			cur.execute('SELECT 1')
			cur.close()
			release_connection(conn)
			return True
		return False
	except Exception as e:
		print(f"Database connection test failed: {e}")
		return False



# Cung cấp đối tượng `db` giống Firestore được hỗ trợ bởi PostgreSQL qua emulator nhẹ.
# Giữ ký hiệu `db` để tương thích với code hiện có sử dụng db.collection(...).
_db_instance = None

def get_db():
    """Return the DB emulator instance (lazy init to avoid circular import)."""
    global _db_instance
    if _db_instance is None and connection_pool:
        try:
            # import ở đây để tránh circular imports
            from Database.emulator import DBEmulator
            _db_instance = DBEmulator()
            print("✓ DB emulator initialized (PostgreSQL backend)")
        except Exception as e:
            print(f"⚠ Could not initialize DB emulator: {e}")
            _db_instance = None
    return _db_instance

# Để tương thích ngược với code sử dụng `from Database.config import db`
# chúng ta cung cấp thuộc tính `db` cấp module qua __getattr__
def __getattr__(name):
    if name == 'db':
        return get_db()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")