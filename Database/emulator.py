"""Minimal Firestore-like emulator backed by PostgreSQL.

This provides a tiny compatibility layer so existing code that calls
`db.collection(...).document(...).set()` and `.stream()` works with
PostgreSQL tables.

It intentionally implements only the operations used by the app.
"""
from types import SimpleNamespace
from Database.config import get_connection, release_connection
import traceback


class DocumentSnapshot(SimpleNamespace):
    def to_dict(self):
        return dict(self.__dict__)


class DocumentReference:
    def __init__(self, collection_name, doc_id=None):
        self.collection = collection_name
        self.id = doc_id

    def set(self, data):
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            if self.collection.lower() in ('tracks', 'tracks'):
                # sử dụng title làm định danh
                title = data.get('title') or self.id
                cur.execute("SELECT track_id FROM tracks WHERE title = %s", (title,))
                row = cur.fetchone()
                if row:
                    cur.execute(
                        "UPDATE tracks SET artist=%s, genre=%s, location=%s, like_count=%s, language=%s WHERE title=%s",
                        (data.get('artist'), data.get('genre'), data.get('location'), data.get('like_count', 0), data.get('Language') or data.get('language'), title)
                    )
                else:
                    cur.execute(
                        "INSERT INTO tracks (title, artist, genre, location, like_count, language) VALUES (%s,%s,%s,%s,%s,%s)",
                        (title, data.get('artist'), data.get('genre'), data.get('location'), data.get('like_count', 0), data.get('Language') or data.get('language'))
                    )
                conn.commit()
            elif self.collection.lower() in ('artist', 'artists'):
                name = self.id
                cur.execute("SELECT artist_id FROM artists WHERE name = %s", (name,))
                row = cur.fetchone()
                if row:
                    cur.execute("UPDATE artists SET image_url=%s WHERE name=%s", (data.get('image_url'), name))
                else:
                    cur.execute("INSERT INTO artists (name, image_url) VALUES (%s,%s)", (name, data.get('image_url')))
                conn.commit()
            elif self.collection.lower() in ('genres', 'genre'):
                name = self.id
                cur.execute("SELECT genre_id FROM genres WHERE genre_name = %s", (name,))
                row = cur.fetchone()
                if row:
                    cur.execute("UPDATE genres SET genre_image=%s WHERE genre_name=%s", (data.get('genre_image'), name))
                else:
                    cur.execute("INSERT INTO genres (genre_name, genre_image) VALUES (%s,%s)", (name, data.get('genre_image')))
                conn.commit()
            elif self.collection.lower() in ('languages', 'language'):
                name = self.id
                cur.execute("SELECT language_id FROM languages WHERE language_name = %s", (name,))
                row = cur.fetchone()
                if row:
                    cur.execute("UPDATE languages SET language_image=%s WHERE language_name=%s", (data.get('language_image'), name))
                else:
                    cur.execute("INSERT INTO languages (language_name, language_image) VALUES (%s,%s)", (name, data.get('language_image')))
                conn.commit()
            elif self.collection.lower() in ('users', 'user'):
                # doc id phải là chuỗi uid; chuyển đổi nếu là số
                uid = self.id
                try:
                    user_id = int(uid)
                except Exception:
                    user_id = None
                # chèn hoặc cập nhật theo user_id hoặc email
                if user_id:
                    cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
                    row = cur.fetchone()
                    if row:
                        cur.execute("UPDATE users SET display_name=%s, email=%s, password=%s, phone_number=%s WHERE user_id=%s",
                                    (data.get('display_name') or data.get('displayName'), data.get('email'), data.get('password'), data.get('phone_number'), user_id))
                    else:
                        cur.execute("INSERT INTO users (user_id, display_name, email, password, phone_number) VALUES (%s,%s,%s,%s,%s)",
                                    (user_id, data.get('display_name') or data.get('displayName'), data.get('email'), data.get('password'), data.get('phone_number')))
                else:
                    # thử chèn theo email
                    cur.execute("SELECT user_id FROM users WHERE email = %s", (data.get('email'),))
                    row = cur.fetchone()
                    if row:
                        cur.execute("UPDATE users SET display_name=%s, password=%s, phone_number=%s WHERE email=%s",
                                    (data.get('display_name') or data.get('displayName'), data.get('password'), data.get('phone_number'), data.get('email')))
                    else:
                        cur.execute("INSERT INTO users (display_name, email, password, phone_number) VALUES (%s,%s,%s,%s)",
                                    (data.get('display_name') or data.get('displayName'), data.get('email'), data.get('password'), data.get('phone_number')))
                conn.commit()
            elif self.collection.startswith('albums'):
                # albums và subcollection được xử lý đơn giản
                album_name = self.id
                cur.execute("SELECT album_id FROM albums WHERE album_title = %s", (album_name,))
                row = cur.fetchone()
                if row:
                    cur.execute("UPDATE albums SET artist=%s WHERE album_title=%s", (data.get('artist'), album_name))
                else:
                    cur.execute("INSERT INTO albums (album_title, artist) VALUES (%s,%s)", (album_name, data.get('artist')))
                conn.commit()
            else:
                # collection không được hỗ trợ -> không làm gì
                pass
        except Exception:
            traceback.print_exc()
        finally:
            if conn:
                release_connection(conn)

    def get(self):
        # Trả về đối tượng giống snapshot
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            if self.collection.lower() in ('tracks', 'tracks'):
                title = self.id
                cur.execute("SELECT title, artist, genre, location, like_count, language FROM tracks WHERE title = %s LIMIT 1", (title,))
                row = cur.fetchone()
                if row:
                    keys = ['title', 'artist', 'genre', 'location', 'like_count', 'Language']
                    data = dict(zip(keys, row))
                    return DocumentSnapshot(**data)
                return DocumentSnapshot()
            elif self.collection.lower() in ('users', 'user'):
                uid = self.id
                try:
                    user_id = int(uid)
                except Exception:
                    user_id = None
                if user_id:
                    cur.execute("SELECT user_id, display_name, email, password, phone_number, created_at FROM users WHERE user_id = %s LIMIT 1", (user_id,))
                else:
                    cur.execute("SELECT user_id, display_name, email, password, phone_number, created_at FROM users WHERE email = %s LIMIT 1", (uid,))
                row = cur.fetchone()
                if row:
                    keys = ['user_id', 'display_name', 'email', 'password', 'phone_number', 'created_at']
                    data = dict(zip(keys, row))
                    return DocumentSnapshot(**data)
                return DocumentSnapshot()
            else:
                return DocumentSnapshot()
        except Exception:
            traceback.print_exc()
            return DocumentSnapshot()
        finally:
            if conn:
                release_connection(conn)


class CollectionReference:
    def __init__(self, name):
        self.name = name

    def document(self, doc_id=None):
        return DocumentReference(self.name, doc_id)

    def stream(self):
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            if self.name.lower() in ('tracks', 'tracks'):
                cur.execute("SELECT title, artist, genre, location, like_count, language FROM tracks")
                rows = cur.fetchall()
                keys = ['title', 'artist', 'genre', 'location', 'like_count', 'Language']
                return [DocumentSnapshot(**dict(zip(keys, r))) for r in rows]
            elif self.name.lower() in ('genres', 'genre'):
                cur.execute("SELECT genre_name, genre_image FROM genres")
                rows = cur.fetchall()
                keys = ['genre_name', 'genre_image']
                return [DocumentSnapshot(**dict(zip(keys, r))) for r in rows]
            elif self.name.lower() in ('languages', 'language'):
                cur.execute("SELECT language_name, language_image FROM languages")
                rows = cur.fetchall()
                keys = ['language_name', 'language_image']
                return [DocumentSnapshot(**dict(zip(keys, r))) for r in rows]
            elif self.name.lower() in ('albums', 'album'):
                cur.execute("SELECT album_title, artist FROM albums")
                rows = cur.fetchall()
                keys = ['album_title', 'artist']
                return [DocumentSnapshot(**dict(zip(keys, r))) for r in rows]
            else:
                return []
        except Exception:
            traceback.print_exc()
            return []
        finally:
            if conn:
                release_connection(conn)


class DBEmulator:
    def collection(self, name):
        # Hỗ trợ đường dẫn lồng như 'artist/<name>/tracks' và 'albums/<name>/tracks'
        return CollectionReference(name)

    # các bí danh tiện lợi
    def __getattr__(self, item):
        if item == 'collection':
            return self.collection
        raise AttributeError(item)
