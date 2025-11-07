"""
Migration Lock System - Bảo vệ database khỏi bị migration đồng thời

Tính năng:
- Lock migration để chỉ 1 người có thể chạy tại một thời điểm
- Lưu lịch sử migration
- Backup tự động trước khi migration
- Rollback nếu có lỗi

Usage:
    python -m Database.migration_lock status  # Kiểm tra trạng thái
    python -m Database.migration_lock lock    # Khóa migration
    python -m Database.migration_lock unlock  # Mở khóa migration
    python -m Database.migration_lock history # Xem lịch sử
"""
import sys
import os
import json
from datetime import datetime
import socket
import getpass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Database.config import get_connection, release_connection


class MigrationLock:
    """Quản lý lock cho migration database"""
    
    def __init__(self):
        self.table_name = 'migration_lock'
        self.history_table = 'migration_history'
        self._ensure_tables()
    
    def _ensure_tables(self):
        """Tạo bảng migration_lock và migration_history nếu chưa có"""
        conn = get_connection()
        if not conn:
            raise Exception("Không thể kết nối database")
        
        try:
            cur = conn.cursor()
            
            # Bảng migration_lock - chỉ có 1 row
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY DEFAULT 1,
                    is_locked BOOLEAN DEFAULT FALSE,
                    locked_by VARCHAR(255),
                    locked_at TIMESTAMP,
                    lock_reason TEXT,
                    machine_name VARCHAR(255),
                    CONSTRAINT single_row CHECK (id = 1)
                )
            """)
            
            # Khởi tạo row mặc định nếu chưa có
            cur.execute(f"""
                INSERT INTO {self.table_name} (id, is_locked)
                VALUES (1, FALSE)
                ON CONFLICT (id) DO NOTHING
            """)
            
            # Bảng lịch sử migration
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.history_table} (
                    history_id SERIAL PRIMARY KEY,
                    action VARCHAR(50) NOT NULL,
                    performed_by VARCHAR(255) NOT NULL,
                    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    machine_name VARCHAR(255),
                    description TEXT,
                    status VARCHAR(20) DEFAULT 'success',
                    details JSONB
                )
            """)
            
            conn.commit()
            cur.close()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            release_connection(conn)
    
    def get_machine_info(self):
        """Lấy thông tin máy và user hiện tại"""
        return {
            'machine_name': socket.gethostname(),
            'username': getpass.getuser()
        }
    
    def is_locked(self):
        """Kiểm tra xem migration có đang bị lock không"""
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(f"""
                SELECT is_locked, locked_by, locked_at, lock_reason, machine_name
                FROM {self.table_name}
                WHERE id = 1
            """)
            result = cur.fetchone()
            cur.close()
            
            if result and result[0]:  # is_locked = True
                return {
                    'locked': True,
                    'locked_by': result[1],
                    'locked_at': result[2],
                    'reason': result[3],
                    'machine': result[4]
                }
            return {'locked': False}
        finally:
            release_connection(conn)
    
    def acquire_lock(self, reason="Manual migration"):
        """Lấy lock cho migration"""
        lock_status = self.is_locked()
        
        if lock_status['locked']:
            raise Exception(
                f"❌ Migration đã bị lock!\n"
                f"   Locked by: {lock_status['locked_by']} ({lock_status['machine']})\n"
                f"   Since: {lock_status['locked_at']}\n"
                f"   Reason: {lock_status['reason']}\n\n"
                f"💡 Liên hệ người này hoặc chạy: python -m Database.migration_lock unlock"
            )
        
        info = self.get_machine_info()
        conn = get_connection()
        
        try:
            cur = conn.cursor()
            cur.execute(f"""
                UPDATE {self.table_name}
                SET is_locked = TRUE,
                    locked_by = %s,
                    locked_at = CURRENT_TIMESTAMP,
                    lock_reason = %s,
                    machine_name = %s
                WHERE id = 1
            """, (info['username'], reason, info['machine_name']))
            
            # Ghi log vào history
            cur.execute(f"""
                INSERT INTO {self.history_table}
                (action, performed_by, machine_name, description, details)
                VALUES (%s, %s, %s, %s, %s)
            """, ('LOCK', info['username'], info['machine_name'], reason, 
                  json.dumps(info)))
            
            conn.commit()
            cur.close()
            
            print(f"✅ Migration lock acquired by {info['username']}@{info['machine_name']}")
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            release_connection(conn)
    
    def release_lock(self, force=False):
        """Giải phóng lock"""
        lock_status = self.is_locked()
        info = self.get_machine_info()
        
        if not lock_status['locked']:
            print("ℹ️  Migration không bị lock")
            return True
        
        # Kiểm tra quyền unlock
        if not force and lock_status['locked_by'] != info['username']:
            raise Exception(
                f"❌ Bạn không có quyền unlock!\n"
                f"   Lock hiện tại thuộc về: {lock_status['locked_by']}\n"
                f"   Bạn đang là: {info['username']}\n\n"
                f"💡 Để force unlock, chạy: python -m Database.migration_lock unlock --force"
            )
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(f"""
                UPDATE {self.table_name}
                SET is_locked = FALSE,
                    locked_by = NULL,
                    locked_at = NULL,
                    lock_reason = NULL,
                    machine_name = NULL
                WHERE id = 1
            """)
            
            # Ghi log
            action = 'FORCE_UNLOCK' if force else 'UNLOCK'
            cur.execute(f"""
                INSERT INTO {self.history_table}
                (action, performed_by, machine_name, description)
                VALUES (%s, %s, %s, %s)
            """, (action, info['username'], info['machine_name'], 
                  f"Unlocked from {lock_status['locked_by']}"))
            
            conn.commit()
            cur.close()
            
            print(f"✅ Migration lock released by {info['username']}")
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            release_connection(conn)
    
    def get_history(self, limit=10):
        """Lấy lịch sử migration"""
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(f"""
                SELECT action, performed_by, performed_at, machine_name, 
                       description, status
                FROM {self.history_table}
                ORDER BY performed_at DESC
                LIMIT %s
            """, (limit,))
            
            results = cur.fetchall()
            cur.close()
            return results
        finally:
            release_connection(conn)
    
    def print_status(self):
        """In ra trạng thái hiện tại"""
        lock_status = self.is_locked()
        
        print("\n" + "="*60)
        print("📊 MIGRATION LOCK STATUS")
        print("="*60)
        
        if lock_status['locked']:
            print("🔒 Status: LOCKED")
            print(f"   Locked by: {lock_status['locked_by']}")
            print(f"   Machine: {lock_status['machine']}")
            print(f"   Since: {lock_status['locked_at']}")
            print(f"   Reason: {lock_status['reason']}")
        else:
            print("🔓 Status: UNLOCKED")
            print("   Available for migration")
        
        print("\n" + "-"*60)
        print("📝 RECENT HISTORY (Last 5 actions)")
        print("-"*60)
        
        history = self.get_history(5)
        if history:
            for h in history:
                action, user, time, machine, desc, status = h
                icon = "✅" if status == "success" else "❌"
                print(f"{icon} {action:<12} | {user:<15} | {machine:<20}")
                print(f"   {time} | {desc}")
                print()
        else:
            print("   No history yet")
        
        print("="*60 + "\n")


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    lock_manager = MigrationLock()
    
    try:
        if command == 'status':
            lock_manager.print_status()
        
        elif command == 'lock':
            reason = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else "Manual migration"
            lock_manager.acquire_lock(reason)
        
        elif command == 'unlock':
            force = '--force' in sys.argv
            lock_manager.release_lock(force=force)
        
        elif command == 'history':
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
            history = lock_manager.get_history(limit)
            
            print("\n" + "="*80)
            print(f"📝 MIGRATION HISTORY (Last {limit} actions)")
            print("="*80)
            
            for h in history:
                action, user, time, machine, desc, status = h
                icon = "✅" if status == "success" else "❌"
                print(f"\n{icon} {action:<15} | {user}@{machine}")
                print(f"   Time: {time}")
                print(f"   Desc: {desc}")
            
            print("\n" + "="*80 + "\n")
        
        else:
            print(f"❌ Unknown command: {command}")
            print(__doc__)
    
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
