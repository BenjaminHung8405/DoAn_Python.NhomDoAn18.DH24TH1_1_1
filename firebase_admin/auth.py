"""Simple shim that provides a subset of firebase_admin.auth backed by PostgreSQL.

Only implements the methods used by this project: create_user, get_user,
get_user_by_email, get_user_by_phone_number.
"""
from types import SimpleNamespace
from Database.config import get_connection, release_connection
from . import _auth_utils
import traceback


def _row_to_user_object(row):
    # hàng: (user_id, display_name, email, password, phone_number, created_at)
    if not row:
        return None
    user_id = row[0]
    return SimpleNamespace(
        uid=str(user_id), 
        user_id=user_id, 
        display_name=row[1], 
        email=row[2], 
        password=row[3], 
        phone_number=row[4],
        email_verified=False  # PostgreSQL không lưu trữ điều này, mặc định là False
    )


def create_user(email, phone_number, password, display_name, email_verified=False):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        # kiểm tra email
        cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            raise _auth_utils.EmailAlreadyExistsError('Email already exists')
        # kiểm tra số điện thoại
        cur.execute("SELECT user_id FROM users WHERE phone_number = %s", (phone_number,))
        if cur.fetchone():
            raise _auth_utils.PhoneNumberAlreadyExistsError('Phone number already exists')

        cur.execute("INSERT INTO users (display_name, email, password, phone_number) VALUES (%s,%s,%s,%s) RETURNING user_id",
                    (display_name, email, password, phone_number))
        uid = cur.fetchone()[0]
        conn.commit()
        return SimpleNamespace(uid=str(uid))
    except Exception:
        # tái phát các ngoại lệ đã biết
        if isinstance(Exception, _auth_utils.EmailAlreadyExistsError):
            raise
        traceback.print_exc()
        raise
    finally:
        if conn:
            release_connection(conn)


def get_user(uid):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            user_id = int(uid)
            cur.execute("SELECT user_id, display_name, email, password, phone_number, created_at FROM users WHERE user_id = %s LIMIT 1", (user_id,))
        except Exception:
            cur.execute("SELECT user_id, display_name, email, password, phone_number, created_at FROM users WHERE email = %s LIMIT 1", (uid,))
        row = cur.fetchone()
        if not row:
            raise _auth_utils.UserNotFoundError('User not found')
        return _row_to_user_object(row)
    finally:
        if conn:
            release_connection(conn)


def get_user_by_email(email):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, display_name, email, password, phone_number, created_at FROM users WHERE email = %s LIMIT 1", (email,))
        row = cur.fetchone()
        if not row:
            raise _auth_utils.UserNotFoundError('User not found')
        return _row_to_user_object(row)
    finally:
        if conn:
            release_connection(conn)


def get_user_by_phone_number(phone):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, display_name, email, password, phone_number, created_at FROM users WHERE phone_number = %s LIMIT 1", (phone,))
        row = cur.fetchone()
        if not row:
            raise _auth_utils.UserNotFoundError('User not found')
        return _row_to_user_object(row)
    finally:
        if conn:
            release_connection(conn)
