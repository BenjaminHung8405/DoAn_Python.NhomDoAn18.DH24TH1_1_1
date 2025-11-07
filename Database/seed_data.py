"""
Seed Data Protection - Bảo vệ dữ liệu mẫu khỏi bị xóa

Script này:
1. Insert dữ liệu mẫu nếu database trống
2. Không overwrite dữ liệu đã có
3. Log mọi thay đổi

Usage:
    python -m Database.seed_data
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Database.config import get_connection, release_connection


def check_table_empty(cur, table_name):
    """Kiểm tra xem bảng có trống không"""
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cur.fetchone()[0]
    return count == 0


def seed_languages():
    """Thêm dữ liệu mẫu cho languages"""
    conn = get_connection()
    if not conn:
        print("❌ Không thể kết nối database")
        return False
    
    try:
        cur = conn.cursor()
        
        if not check_table_empty(cur, 'languages'):
            print("ℹ️  Bảng languages đã có dữ liệu, bỏ qua seed")
            return True
        
        languages = [
            ('Vietnamese', 'https://example.com/images/vn.png'),
            ('English', 'https://example.com/images/en.png'),
            ('Korean', 'https://example.com/images/kr.png'),
            ('Japanese', 'https://example.com/images/jp.png'),
            ('Chinese', 'https://example.com/images/cn.png'),
        ]
        
        for lang_name, lang_image in languages:
            cur.execute("""
                INSERT INTO languages (language_name, language_image)
                VALUES (%s, %s)
                ON CONFLICT (language_name) DO NOTHING
            """, (lang_name, lang_image))
        
        conn.commit()
        print(f"✅ Seeded {len(languages)} languages")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error seeding languages: {e}")
        return False
    finally:
        cur.close()
        release_connection(conn)


def seed_genres():
    """Thêm dữ liệu mẫu cho genres"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        if not check_table_empty(cur, 'genres'):
            print("ℹ️  Bảng genres đã có dữ liệu, bỏ qua seed")
            return True
        
        genres = [
            ('Pop', 'https://example.com/images/pop.png'),
            ('Rock', 'https://example.com/images/rock.png'),
            ('Hip Hop', 'https://example.com/images/hiphop.png'),
            ('Jazz', 'https://example.com/images/jazz.png'),
            ('Classical', 'https://example.com/images/classical.png'),
            ('EDM', 'https://example.com/images/edm.png'),
            ('R&B', 'https://example.com/images/rnb.png'),
            ('Country', 'https://example.com/images/country.png'),
        ]
        
        for genre_name, genre_image in genres:
            cur.execute("""
                INSERT INTO genres (genre_name, genre_image)
                VALUES (%s, %s)
                ON CONFLICT (genre_name) DO NOTHING
            """, (genre_name, genre_image))
        
        conn.commit()
        print(f"✅ Seeded {len(genres)} genres")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error seeding genres: {e}")
        return False
    finally:
        cur.close()
        release_connection(conn)


def seed_artists():
    """Thêm dữ liệu mẫu cho artists"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        if not check_table_empty(cur, 'artists'):
            print("ℹ️  Bảng artists đã có dữ liệu, bỏ qua seed")
            return True
        
        artists = [
            ('Sơn Tùng M-TP', 'https://example.com/images/sontung.png'),
            ('Đen Vâu', 'https://example.com/images/denvau.png'),
            ('Hồ Ngọc Hà', 'https://example.com/images/hongocha.png'),
            ('Mỹ Tâm', 'https://example.com/images/mytam.png'),
            ('The Weeknd', 'https://example.com/images/theweeknd.png'),
            ('Taylor Swift', 'https://example.com/images/taylorswift.png'),
            ('BTS', 'https://example.com/images/bts.png'),
            ('BlackPink', 'https://example.com/images/blackpink.png'),
        ]
        
        for artist_name, artist_image in artists:
            cur.execute("""
                INSERT INTO artists (name, image_url)
                VALUES (%s, %s)
                ON CONFLICT (name) DO NOTHING
            """, (artist_name, artist_image))
        
        conn.commit()
        print(f"✅ Seeded {len(artists)} artists")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error seeding artists: {e}")
        return False
    finally:
        cur.close()
        release_connection(conn)


def seed_sample_tracks():
    """Thêm một vài bài hát mẫu"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        if not check_table_empty(cur, 'tracks'):
            print("ℹ️  Bảng tracks đã có dữ liệu, bỏ qua seed")
            return True
        
        tracks = [
            ('Lạc Trôi', 'Sơn Tùng M-TP', 'Pop', 'Vietnamese', 
             'https://example.com/music/lac-troi.mp3', 100000),
            ('Bài Này Chill Phết', 'Đen Vâu', 'Hip Hop', 'Vietnamese',
             'https://example.com/music/bai-nay-chill-phet.mp3', 85000),
            ('Blinding Lights', 'The Weeknd', 'Pop', 'English',
             'https://example.com/music/blinding-lights.mp3', 150000),
            ('Dynamite', 'BTS', 'Pop', 'Korean',
             'https://example.com/music/dynamite.mp3', 120000),
        ]
        
        for title, artist, genre, language, location, like_count in tracks:
            cur.execute("""
                INSERT INTO tracks (title, artist, genre, language, location, like_count)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (title) DO NOTHING
            """, (title, artist, genre, language, location, like_count))
        
        conn.commit()
        print(f"✅ Seeded {len(tracks)} sample tracks")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error seeding tracks: {e}")
        return False
    finally:
        cur.close()
        release_connection(conn)


def seed_all():
    """Seed tất cả dữ liệu mẫu"""
    print("\n" + "="*60)
    print("🌱 SEEDING DATABASE")
    print("="*60 + "\n")
    
    success = True
    success = seed_languages() and success
    success = seed_genres() and success
    success = seed_artists() and success
    success = seed_sample_tracks() and success
    
    print("\n" + "="*60)
    if success:
        print("✅ Database seeding completed successfully!")
    else:
        print("⚠️  Some seeding operations failed")
    print("="*60 + "\n")
    
    return success


def show_stats():
    """Hiển thị thống kê database"""
    conn = get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        tables = ['users', 'tracks', 'artists', 'genres', 'languages', 'albums']
        
        print("\n" + "="*60)
        print("📊 DATABASE STATISTICS")
        print("="*60 + "\n")
        
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"  {table:<15} : {count:>5} records")
        
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
    finally:
        cur.close()
        release_connection(conn)


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Seed database with sample data')
    parser.add_argument('command', nargs='?', default='seed',
                       choices=['seed', 'stats'],
                       help='Command to run (default: seed)')
    
    args = parser.parse_args()
    
    if args.command == 'seed':
        seed_all()
    elif args.command == 'stats':
        show_stats()


if __name__ == '__main__':
    main()
