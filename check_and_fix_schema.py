#!/usr/bin/env python3
"""
Script kiểm tra và sửa schema database cho ứng dụng Amplify
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Database.config import get_connection

def check_current_schema():
    """Kiểm tra schema hiện tại của database"""
    print("🔍 Đang kiểm tra schema database hiện tại...\n")
    
    conn = get_connection()
    if not conn:
        print("❌ Không thể kết nối database!")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Lấy danh sách các bảng
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        
        print("📋 Các bảng hiện có trong database:")
        for table in tables:
            print(f"  - {table}")
        
        print(f"\n✓ Tổng cộng: {len(tables)} bảng")
        
        # Kiểm tra các bảng cần thiết cho Amplify
        required_tables = ['users', 'tracks', 'artists', 'genres', 'languages', 'albums', 'user_likes']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"\n⚠️  Thiếu các bảng cần thiết: {', '.join(missing_tables)}")
            return False
        else:
            print(f"\n✅ Tất cả các bảng cần thiết đều có!")
            return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def show_current_database_info():
    """Hiển thị thông tin database hiện tại"""
    conn = get_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Lấy tên database
        cursor.execute("SELECT current_database()")
        db_name = cursor.fetchone()[0]
        
        # Lấy user
        cursor.execute("SELECT current_user")
        db_user = cursor.fetchone()[0]
        
        # Lấy host
        cursor.execute("SELECT inet_server_addr()")
        result = cursor.fetchone()
        db_host = result[0] if result and result[0] else "localhost"
        
        print("\n" + "="*60)
        print("📊 THÔNG TIN DATABASE HIỆN TẠI")
        print("="*60)
        print(f"Database: {db_name}")
        print(f"User: {db_user}")
        print(f"Host: {db_host}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Không thể lấy thông tin database: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    print("="*60)
    print("🔧 KIỂM TRA VÀ SỬA SCHEMA DATABASE")
    print("="*60 + "\n")
    
    # Hiển thị thông tin database
    show_current_database_info()
    
    # Kiểm tra schema
    is_correct = check_current_schema()
    
    if not is_correct:
        print("\n" + "="*60)
        print("⚠️  DATABASE KHÔNG ĐÚNG SCHEMA!")
        print("="*60)
        print("\n📝 Bạn có 2 lựa chọn:")
        print("1. Tạo database mới cho Amplify trên Neon")
        print("2. Chạy script reset_schema.py để khởi tạo lại schema")
        print("\n💡 Khuyến nghị: Tạo database mới để tránh xung đột dữ liệu")
        print("\nCách tạo database mới:")
        print("  1. Truy cập https://console.neon.tech")
        print("  2. Tạo project mới hoặc database mới")
        print("  3. Copy connection string")
        print("  4. Cập nhật DATABASE_URL trong file .env")
        print("  5. Chạy: python Database/reset_schema.py")
    else:
        print("\n" + "="*60)
        print("✅ DATABASE ĐÚNG SCHEMA - SẴN SÀNG SỬ DỤNG!")
        print("="*60)

if __name__ == "__main__":
    main()
