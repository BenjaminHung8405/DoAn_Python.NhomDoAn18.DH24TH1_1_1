from Database.config import get_connection, release_connection
import traceback
import tkinter as tk
from tkinter import messagebox
import hashlib
import os


def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_artist(artist):
    """Returns boolean value if the artist exists or not in the database"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM artists WHERE name = %s", (artist,))
        result = cursor.fetchone()
        cursor.close()
        print('Artist checked successfully')
        return result is not None
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def check_genre(genre):
    """Returns boolean value if the genre exists or not in the database"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM genres WHERE genre_name = %s", (genre,))
        result = cursor.fetchone()
        cursor.close()
        print('Genre checked successfully')
        return result is not None
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def check_language(language):
    """Returns boolean value if the language exists or not in the database"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM languages WHERE language_name = %s", (language,))
        result = cursor.fetchone()
        cursor.close()
        print('Language checked successfully')
        return result is not None
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def set_language(language, language_image=''):
    """Add a new language to the database"""
    conn = None
    try:
        if check_language(language):
            return True
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO languages (language_name, language_image) VALUES (%s, %s)",
            (language, language_image)
        )
        conn.commit()
        cursor.close()
        return True
    except Exception as ex:
        if conn:
            conn.rollback()
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def get_tracks_by_language(**kwargs):
    """
    Returns a list of songs with particular language
    kwarg: language = 'required language'
    else return the list of all languages
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if 'language' in kwargs:
            cursor.execute("""
                SELECT track_id, title, artist, genre, location, like_count, language
                FROM tracks
                WHERE language = %s
            """, (kwargs['language'],))
            
            columns = [desc[0] for desc in cursor.description]
            tracks = []
            for row in cursor.fetchall():
                track_dict = dict(zip(columns, row))
                tracks.append(track_dict)
            cursor.close()
            return tracks
        else:
            cursor.execute("SELECT language_name, language_image FROM languages")
            columns = [desc[0] for desc in cursor.description]
            languages = []
            for row in cursor.fetchall():
                lang_dict = {
                    'text': row[0],
                    'url': row[1] or ''
                }
                languages.append(lang_dict)
            cursor.close()
            return languages
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def set_artist(track_title, track_genre, track_location, track_artist, language):
    """Function to set artist details and add track"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Add artist if not exists
        if not check_artist(track_artist):
            cursor.execute(
                "INSERT INTO artists (name, image_url) VALUES (%s, %s)",
                (track_artist, '')
            )
        
        # Add track
        cursor.execute("""
            INSERT INTO tracks (title, artist, genre, location, language, like_count)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (title, artist) DO NOTHING
        """, (track_title, track_artist, track_genre, track_location, language, 0))
        
        conn.commit()
        cursor.close()
        print('Artist and track added successfully')
        return True
    except Exception as ex:
        if conn:
            conn.rollback()
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def get_artist_tracks(artist):
    """Returns a list of track objects for the given artist"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT track_id, title, artist, genre, location, like_count, language
            FROM tracks
            WHERE artist = %s
        """, (artist,))
        
        columns = [desc[0] for desc in cursor.description]
        tracks = []
        for row in cursor.fetchall():
            track_dict = dict(zip(columns, row))
            tracks.append(track_dict)
        cursor.close()
        return tracks
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def get_all_artists():
    """Returns a list of all artists"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT artist_id, name, image_url FROM artists")
        
        columns = [desc[0] for desc in cursor.description]
        artists = []
        for row in cursor.fetchall():
            artist_dict = dict(zip(columns, row))
            artists.append({
                'text': artist_dict['name'],
                'url': artist_dict.get('image_url', '')
            })
        cursor.close()
        return artists
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def get_all_tracks():
    """Returns a list of all tracks"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT track_id, title, artist, genre, location, language, like_count FROM tracks")
        
        columns = [desc[0] for desc in cursor.description]
        tracks = []
        for row in cursor.fetchall():
            track_dict = dict(zip(columns, row))
            tracks.append(track_dict)
        cursor.close()
        return tracks
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def get_tracks_by_genre(genre):
    """Returns a list of tracks for a given genre"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT track_id, title, artist, genre, location, like_count, language
            FROM tracks
            WHERE genre = %s
        """, (genre,))
        
        columns = [desc[0] for desc in cursor.description]
        tracks = []
        for row in cursor.fetchall():
            track_dict = dict(zip(columns, row))
            tracks.append(track_dict)
        cursor.close()
        return tracks
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def get_all_genres():
    """Returns a list of all genres"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT genre_name, genre_image FROM genres")
        
        columns = [desc[0] for desc in cursor.description]
        genres = []
        for row in cursor.fetchall():
            genre_dict = {
                'text': row[0],
                'url': row[1] or ''
            }
            genres.append(genre_dict)
        cursor.close()
        return genres
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def get_genre(genre_name):
    """Get genre by name"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT genre_name, genre_image FROM genres WHERE genre_name = %s", (genre_name,))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {
                'genre_name': result[0],
                'genre_image': result[1] or ''
            }
        return None
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def get_artist(artist_name):
    """Get artist by name"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, image_url FROM artists WHERE name = %s", (artist_name,))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {
                'name': result[0],
                'image_url': result[1] or ''
            }
        return None
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def get_user(user_id):
    """Get user by ID"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, display_name, email, created_at, phone_number
            FROM users
            WHERE user_id = %s
        """, (user_id,))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {
                'user_id': result[0],
                'display_name': result[1],
                'email': result[2],
                'created_at': result[3],
                'phone_number': result[4]
            }
        return None
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return None
    finally:
        if conn:
            release_connection(conn)


def create_user(email, password, display_name, phone_number=None):
    """Create a new user"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute("""
            INSERT INTO users (email, password_hash, display_name, phone_number)
            VALUES (%s, %s, %s, %s)
            RETURNING user_id
        """, (email, password_hash, display_name, phone_number))
        
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        
        print(f'User created successfully with ID: {user_id}')
        return user_id
    except Exception as ex:
        if conn:
            conn.rollback()
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return None
    finally:
        if conn:
            release_connection(conn)


def verify_user(email, password):
    """Verify user credentials"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute("""
            SELECT user_id, display_name, email
            FROM users
            WHERE email = %s AND password_hash = %s
        """, (email, password_hash))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {
                'user_id': result[0],
                'display_name': result[1],
                'email': result[2]
            }
        return None
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return None
    finally:
        if conn:
            release_connection(conn)


def get_trending_tracks(limit=20):
    """Get trending tracks sorted by like count"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT track_id, title, artist, genre, location, like_count, language
            FROM tracks
            ORDER BY like_count DESC
            LIMIT %s
        """, (limit,))
        
        columns = [desc[0] for desc in cursor.description]
        tracks = []
        for row in cursor.fetchall():
            track_dict = dict(zip(columns, row))
            tracks.append(track_dict)
        cursor.close()
        return tracks
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return []
    finally:
        if conn:
            release_connection(conn)


def search_tracks(query):
    """Search tracks by title or artist"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        search_pattern = f'%{query}%'
        cursor.execute("""
            SELECT track_id, title, artist, genre, location, like_count, language
            FROM tracks
            WHERE title ILIKE %s OR artist ILIKE %s
            ORDER BY like_count DESC
        """, (search_pattern, search_pattern))
        
        columns = [desc[0] for desc in cursor.description]
        tracks = []
        for row in cursor.fetchall():
            track_dict = dict(zip(columns, row))
            tracks.append(track_dict)
        cursor.close()
        return tracks
    except Exception as ex:
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return []
    finally:
        if conn:
            release_connection(conn)


def like_track(track_id):
    """Increment like count for a track"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tracks
            SET like_count = like_count + 1
            WHERE track_id = %s
        """, (track_id,))
        conn.commit()
        cursor.close()
        return True
    except Exception as ex:
        if conn:
            conn.rollback()
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def unlike_track(track_id):
    """Decrement like count for a track"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tracks
            SET like_count = GREATEST(like_count - 1, 0)
            WHERE track_id = %s
        """, (track_id,))
        conn.commit()
        cursor.close()
        return True
    except Exception as ex:
        if conn:
            conn.rollback()
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return False
    finally:
        if conn:
            release_connection(conn)


def Forget_password_email(email):
    """Send forget password email - stub implementation"""
    # For now, just show a message
    messagebox.showinfo("Forget Password", "Password reset feature not implemented yet.")

def get_all_liked_songs(uid):
    """Get all liked songs for a user"""
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.track_id, t.title, t.artist, t.genre, t.location, t.language, t.like_count
            FROM tracks t
            JOIN user_liked_tracks ult ON t.track_id = ult.track_id
            WHERE ult.user_id = %s
            ORDER BY ult.liked_at DESC
        """, (uid,))
        
        columns = [desc[0] for desc in cursor.description]
        tracks = []
        for row in cursor.fetchall():
            track_dict = dict(zip(columns, row))
            tracks.append(track_dict)
        cursor.close()
        return tracks
    except Exception as ex:
        print('Exception in get_all_liked_songs:', ex)
        # If table doesn't exist, return empty list
        if 'UndefinedTable' in str(ex) or 'user_liked_tracks' in str(ex):
            return []
        messagebox.showerror('Error', 'Oops!! Something went wrong!!\nTry again later.')
        print('Exception Occurred which is of type:', ex.__class__.__name__)
        traceback.print_exc()
        return []
    finally:
        if conn:
            release_connection(conn)


def sign_out():
    """Sign out by removing the user file"""
    try:
        os.remove("user")
        return True
    except Exception as ex:
        print('Exception in sign_out:', ex)
        return False
