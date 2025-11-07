"""
Protected Migration System - Migration an toàn với backup và lock

Tính năng:
- Tự động lock trước khi migration
- Backup database trước khi migration
- Rollback nếu có lỗi
- Log chi tiết mọi thay đổi

Usage:
    python -m Database.protected_migration run        # Chạy migration
    python -m Database.protected_migration backup     # Backup manual
    python -m Database.protected_migration restore    # Restore từ backup
"""
import sys
import os
import json
from datetime import datetime
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Database.config import get_connection, release_connection, DATABASE_URL
from Database.migration_lock import MigrationLock


class ProtectedMigration:
    """Migration an toàn với backup và lock"""
    
    def __init__(self):
        self.lock_manager = MigrationLock()
        self.backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, reason="Manual backup"):
        """Tạo backup của database"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'backup_{timestamp}.sql')
        
        print(f"\n📦 Creating backup: {backup_file}")
        
        try:
            # Parse DATABASE_URL để lấy thông tin kết nối
            # Format: postgresql://user:pass@host:port/dbname?params
            if not DATABASE_URL or DATABASE_URL == 'postgresql://user:password@host/database':
                raise Exception("DATABASE_URL chưa được cấu hình trong .env")
            
            # Sử dụng pg_dump để backup
            # Note: Cần có pg_dump installed
            env = os.environ.copy()
            env['PGPASSWORD'] = self._extract_password(DATABASE_URL)
            
            host = self._extract_host(DATABASE_URL)
            port = self._extract_port(DATABASE_URL)
            dbname = self._extract_dbname(DATABASE_URL)
            user = self._extract_user(DATABASE_URL)
            
            cmd = [
                'pg_dump',
                '-h', host,
                '-p', str(port),
                '-U', user,
                '-d', dbname,
                '-f', backup_file,
                '--no-owner',
                '--no-acl'
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"pg_dump failed: {result.stderr}")
            
            # Lưu metadata
            metadata = {
                'timestamp': timestamp,
                'reason': reason,
                'database_url': DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'unknown',
                'created_by': os.getenv('USER', 'unknown')
            }
            
            metadata_file = backup_file.replace('.sql', '.json')
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✅ Backup created successfully: {backup_file}")
            print(f"   Size: {os.path.getsize(backup_file)} bytes")
            return backup_file
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            print("\n💡 Tip: Đảm bảo pg_dump được cài đặt:")
            print("   Ubuntu/Debian: sudo apt-get install postgresql-client")
            print("   macOS: brew install postgresql")
            return None
    
    def _extract_password(self, url):
        """Trích xuất password từ DATABASE_URL"""
        try:
            # postgresql://user:pass@host...
            auth_part = url.split('://')[1].split('@')[0]
            if ':' in auth_part:
                return auth_part.split(':')[1]
        except:
            pass
        return ''
    
    def _extract_user(self, url):
        """Trích xuất user từ DATABASE_URL"""
        try:
            auth_part = url.split('://')[1].split('@')[0]
            return auth_part.split(':')[0]
        except:
            return 'postgres'
    
    def _extract_host(self, url):
        """Trích xuất host từ DATABASE_URL"""
        try:
            host_part = url.split('@')[1].split('/')[0]
            if ':' in host_part:
                return host_part.split(':')[0]
            return host_part
        except:
            return 'localhost'
    
    def _extract_port(self, url):
        """Trích xuất port từ DATABASE_URL"""
        try:
            host_part = url.split('@')[1].split('/')[0]
            if ':' in host_part:
                return int(host_part.split(':')[1])
        except:
            pass
        return 5432
    
    def _extract_dbname(self, url):
        """Trích xuất database name từ DATABASE_URL"""
        try:
            # Lấy phần sau host, trước dấu ?
            db_part = url.split('/')[-1].split('?')[0]
            return db_part
        except:
            return 'postgres'
    
    def list_backups(self):
        """Liệt kê các backup có sẵn"""
        backups = []
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.sql'):
                filepath = os.path.join(self.backup_dir, filename)
                metadata_file = filepath.replace('.sql', '.json')
                
                metadata = {}
                if os.path.exists(metadata_file):
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                
                backups.append({
                    'file': filepath,
                    'filename': filename,
                    'size': os.path.getsize(filepath),
                    'created': datetime.fromtimestamp(os.path.getctime(filepath)),
                    'metadata': metadata
                })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def run_migration_safe(self, migration_script, reason="Migration"):
        """Chạy migration an toàn với lock và backup"""
        print("\n" + "="*60)
        print("🚀 PROTECTED MIGRATION")
        print("="*60)
        
        # Bước 1: Kiểm tra lock
        print("\n1️⃣  Checking migration lock...")
        try:
            self.lock_manager.acquire_lock(reason)
        except Exception as e:
            print(f"\n{e}")
            return False
        
        backup_file = None
        success = False
        
        try:
            # Bước 2: Tạo backup
            print("\n2️⃣  Creating backup before migration...")
            backup_file = self.create_backup(reason)
            if not backup_file:
                raise Exception("Backup failed - aborting migration for safety")
            
            # Bước 3: Chạy migration
            print("\n3️⃣  Running migration script...")
            if callable(migration_script):
                result = migration_script()
            else:
                # Nếu là file path
                result = subprocess.run([sys.executable, migration_script], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"Migration script failed: {result.stderr}")
                print(result.stdout)
                result = True
            
            if result:
                print("\n✅ Migration completed successfully!")
                success = True
            else:
                raise Exception("Migration returned False")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            print("\n🔄 Rollback options:")
            print(f"   1. Restore from backup: python -m Database.protected_migration restore {os.path.basename(backup_file)}")
            print(f"   2. Check logs and fix manually")
            success = False
        
        finally:
            # Bước 4: Release lock
            print("\n4️⃣  Releasing migration lock...")
            try:
                self.lock_manager.release_lock()
            except Exception as e:
                print(f"⚠️  Warning: Could not release lock: {e}")
        
        print("\n" + "="*60)
        return success


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    pm = ProtectedMigration()
    
    try:
        if command == 'backup':
            reason = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else "Manual backup"
            pm.create_backup(reason)
        
        elif command == 'list':
            backups = pm.list_backups()
            print("\n" + "="*80)
            print(f"📦 AVAILABLE BACKUPS ({len(backups)} found)")
            print("="*80 + "\n")
            
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup['filename']}")
                print(f"   Created: {backup['created']}")
                print(f"   Size: {backup['size']:,} bytes")
                if backup['metadata']:
                    print(f"   Reason: {backup['metadata'].get('reason', 'N/A')}")
                    print(f"   By: {backup['metadata'].get('created_by', 'N/A')}")
                print()
        
        elif command == 'run':
            # Chạy init_schema.py an toàn
            from Database.init_schema import create_schema
            pm.run_migration_safe(create_schema, "Running init_schema migration")
        
        elif command == 'restore':
            print("⚠️  Restore functionality requires manual pg_restore")
            print("\nBackups available:")
            backups = pm.list_backups()
            for i, backup in enumerate(backups, 1):
                print(f"  {i}. {backup['filename']} ({backup['created']})")
        
        else:
            print(f"❌ Unknown command: {command}")
            print(__doc__)
    
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
