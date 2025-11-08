from Database.config import *
import traceback
import tkinter as tk
from tkinter import messagebox


def Check_artist(artist):
	"""
	Returns boolean value if the artist exist or not in the database
	"""
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		cur.execute("SELECT artist_id FROM artists WHERE name = %s", (artist,))
		result = cur.fetchone()
		cur.close()
		
		if result is None:
			return False
		print('Artist got successfully')
		return True
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)

def Check_genre(genre):
	"""
	Returns boolean value if the genre exist or not in the database
	"""
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		cur.execute("SELECT genre_id FROM genres WHERE name = %s", (genre,))
		result = cur.fetchone()
		cur.close()
		
		if result is None:
		   return False
		print('genre got successfully')
		return True
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)

def Check_language(language):
	"""
	Returns boolean value if the language exist or not in the database
	"""
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		cur.execute("SELECT language_id FROM languages WHERE name = %s", (language,))
		result = cur.fetchone()
		cur.close()
		
		if result is None:
		   return False
		print('language got successfully')
		return True
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)

def set_language(language):
	'''


	:param language:
	This is the name of the language

	:return:
	Bool if success

	'''
	conn = None
	try:
		if(Check_language(language)):
			pass
		else : 
			conn = get_connection()
			cur = conn.cursor()
			cur.execute("INSERT INTO languages (name) VALUES (%s)", (language,))
			conn.commit()
			cur.close()
		return True
	except Exception as ex:
		if conn:
			conn.rollback()
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)
def get_tracks_by_language(**kwargs):
	"""
	Returns a list of songs with particular language
	kwarg : language = 'required language'
	else return the list of all languages
	if failed returns false
	"""
	conn = None
	if 'language' in kwargs:
		try:
			conn = get_connection()
			cur = conn.cursor()
			cur.execute("""
				SELECT t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count,
					   a.name as artist_name, al.title as album_title, g.name as genre_name, l.name as language_name
				FROM tracks t
				LEFT JOIN languages l ON t.language_id = l.language_id
				LEFT JOIN genres g ON t.genre_id = g.genre_id
				LEFT JOIN albums al ON t.album_id = al.album_id
				LEFT JOIN track_artists ta ON t.track_id = ta.track_id
				LEFT JOIN artists a ON ta.artist_id = a.artist_id
				WHERE l.name = %s
			""", (kwargs['language'],))
			
			rows = cur.fetchall()
			cur.close()
			
			if len(rows):
				object_list = []
				for row in rows:
					track_dict = {
						'track_id': row[0],
						'title': row[1],
						'duration_seconds': row[2],
						'location': row[3],
						'like_count': row[4],
						'artist': row[5],
						'album': row[6],
						'genre': row[7],
						'language': row[8]
					}
					object_list.append(track_dict)
				return object_list
			return []
		except Exception as ex:
			messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
			print('Exception Occurred which is of type :', ex.__class__.__name__)
			y = input('If you want to see Traceback press 1 : ')
			if y == '1':
				traceback.print_exc()
			return []
		finally:
			if conn:
				release_connection(conn)
	else:
		try:
			# Truy vấn bảng languages của PostgreSQL
			conn = get_connection()
			if not conn:
				return []
			
			cur = conn.cursor()
			cur.execute("SELECT name FROM languages")
			rows = cur.fetchall()
			cur.close()
			
			all_dicts = []
			for row in rows:
				my_dict = {
					'text': row[0],  # tên ngôn ngữ
					'url': '',   # hình ảnh ngôn ngữ (empty for now)
				}
				all_dicts.append(my_dict)
			return all_dicts
		except Exception as ex:
			messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
			print('Exception Occurred which is of type :', ex.__class__.__name__)
			y = input('If you want to see Traceback press 1 : ')
			if y == '1':
				traceback.print_exc()
			return []
		finally:
			if conn:
				release_connection(conn)
def set_artist(track_title, track_genre, track_location, track_artist, language):
	"""
	Function to set only artist details
	Returns boolean True if set else False
	gets invoked in the get song function
	"""
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		# Check if artist exists, if not create it
		cur.execute("SELECT artist_id FROM artists WHERE name = %s", (track_artist,))
		artist_result = cur.fetchone()
		
		if not artist_result:
			cur.execute("INSERT INTO artists (name, image_url) VALUES (%s, %s) RETURNING artist_id", 
					   (track_artist, ''))
			artist_id = cur.fetchone()[0]
		else:
			artist_id = artist_result[0]
		
		# Get genre_id
		cur.execute("SELECT genre_id FROM genres WHERE name = %s", (track_genre,))
		genre_result = cur.fetchone()
		genre_id = genre_result[0] if genre_result else None
		
		# Get language_id
		cur.execute("SELECT language_id FROM languages WHERE name = %s", (language,))
		language_result = cur.fetchone()
		language_id = language_result[0] if language_result else None
		
		# Insert track
		cur.execute("""
			INSERT INTO tracks (title, duration_seconds, location_url, genre_id, language_id) 
			VALUES (%s, %s, %s, %s, %s) RETURNING track_id
		""", (track_title, 0, track_location, genre_id, language_id))
		track_id = cur.fetchone()[0]
		
		# Insert track-artist relationship
		cur.execute("INSERT INTO track_artists (track_id, artist_id) VALUES (%s, %s)", 
				   (track_id, artist_id))
		
		conn.commit()
		cur.close()
		
		print('artist added')
		return True
	except Exception as ex:
		if conn:
			conn.rollback()
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)
def get_artist_tracks(artist):
	"""
	Returns a list of the objects of tracks
	if the artist exist or else returns False

	"""
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		cur.execute("""
			SELECT t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count,
				   a.name as artist_name, g.name as genre_name, l.name as language_name
			FROM tracks t
			JOIN track_artists ta ON t.track_id = ta.track_id
			JOIN artists a ON ta.artist_id = a.artist_id
			LEFT JOIN genres g ON t.genre_id = g.genre_id
			LEFT JOIN languages l ON t.language_id = l.language_id
			WHERE a.name = %s
		""", (artist,))
		
		rows = cur.fetchall()
		cur.close()
		
		if not rows:
			return False
			
		tracks = []
		for row in rows:
			track_dict = {
				'track_id': row[0],
				'title': row[1],
				'duration_seconds': row[2],
				'location': row[3],
				'like_count': row[4],
				'artist': row[5],
				'genre': row[6],
				'Language': row[7]
			}
			tracks.append(track_dict)
		
		return tracks
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)
def set_track(track_title, track_genre, track_location, track_artist, language):
	"""
	Function to set only track details
	Returns boolean depending if the value is successfully set then 'True' else 'False'

	"""
	if track_artist == '' or track_genre == '' or track_location == '' or track_title == '':
		raise Exception('Cannot generate with empty Field')
	
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		# Get or create artist
		cur.execute("SELECT artist_id FROM artists WHERE name = %s", (track_artist,))
		artist_result = cur.fetchone()
		if not artist_result:
			cur.execute("INSERT INTO artists (name, image_url) VALUES (%s, %s) RETURNING artist_id", 
					   (track_artist, ''))
			artist_id = cur.fetchone()[0]
		else:
			artist_id = artist_result[0]
		
		# Get genre_id
		cur.execute("SELECT genre_id FROM genres WHERE name = %s", (track_genre,))
		genre_result = cur.fetchone()
		genre_id = genre_result[0] if genre_result else None
		
		# Get language_id
		cur.execute("SELECT language_id FROM languages WHERE name = %s", (language,))
		language_result = cur.fetchone()
		language_id = language_result[0] if language_result else None
		
		# Insert track
		cur.execute("""
			INSERT INTO tracks (title, duration_seconds, location_url, genre_id, language_id) 
			VALUES (%s, %s, %s, %s, %s) RETURNING track_id
		""", (track_title, 0, track_location, genre_id, language_id))
		track_id = cur.fetchone()[0]
		
		# Insert track-artist relationship
		cur.execute("INSERT INTO track_artists (track_id, artist_id) VALUES (%s, %s)", 
				   (track_id, artist_id))
		
		conn.commit()
		cur.close()
		
		print('Track added successfully')
		set_genre(track_genre)
		set_language(language)
		return True
	except Exception as ex:
		if conn:
			conn.rollback()
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)
def get_track(trackName):
	"""
	Fetch particular track for user
	returns dictitonary with the keys as
	artist, genre, location , title
	if failed returns false
	"""
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		cur.execute("""
			SELECT t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count,
				   a.name as artist, g.name as genre, l.name as Language
			FROM tracks t
			LEFT JOIN track_artists ta ON t.track_id = ta.track_id
			LEFT JOIN artists a ON ta.artist_id = a.artist_id
			LEFT JOIN genres g ON t.genre_id = g.genre_id
			LEFT JOIN languages l ON t.language_id = l.language_id
			WHERE t.title = %s
			LIMIT 1
		""", (trackName,))
		
		row = cur.fetchone()
		cur.close()
		
		if not row:
			return False
			
		track_dict = {
			'track_id': row[0],
			'title': row[1],
			'duration_seconds': row[2],
			'location': row[3],
			'like_count': row[4],
			'artist': row[5],
			'genre': row[6],
			'Language': row[7]
		}
		
		return track_dict
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)
def register_user(username, email, phone, password):
	"""
	Returns user uid if successfully registered
	else returns false
	"""
	import psycopg2
	from psycopg2 import IntegrityError
	import hashlib
	
	try:
		if username == '' or email == '':
			raise Exception('Some of fields were found to be empty')
		elif len(password) <= 6:
			raise Exception('Password length less then equal to 6')
		
		# Hash password
		hashed_password = hashlib.sha256(password.encode()).hexdigest()
		
		# Tạo người dùng trong PostgreSQL
		conn = get_connection()
		if not conn:
			raise Exception('Database connection failed')
		
		cur = conn.cursor()
		cur.execute("""
			INSERT INTO users (display_name, email, phone_number, password_hash, created_at)
			VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
			RETURNING user_id
		""", (username, email, phone, hashed_password))
		
		user_id = cur.fetchone()[0]
		conn.commit()
		cur.close()
		release_connection(conn)
		
		print('Successfully created new user: {0}'.format(user_id))
		return str(user_id)
		
	except IntegrityError as ex:
		# Email đã tồn tại (UNIQUE constraint)
		if conn:
			conn.rollback()
			release_connection(conn)
		messagebox.showerror('Error', 'Email already exists! Please use a different email.')
		print('Registration failed: Email already exists')
		return False
	except psycopg2.errors.UniqueViolation as ex:
		# Số điện thoại đã tồn tại
		messagebox.showerror('Error', 'Phone number already exists! Please use a different phone.')
		print('Registration failed: Phone number already exists')
		return False
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		print(str(ex))
		return False


def set_album(track_title, album_name, artist):
	"""
	Returns boolean value depending upon success
	and atleast one track is needed for the album.
	"""
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		# Get or create artist
		cur.execute("SELECT artist_id FROM artists WHERE name = %s", (artist,))
		artist_result = cur.fetchone()
		if not artist_result:
			cur.execute("INSERT INTO artists (name, image_url) VALUES (%s, %s) RETURNING artist_id", 
					   (artist, ''))
			artist_id = cur.fetchone()[0]
		else:
			artist_id = artist_result[0]
		
		# Create or get album
		cur.execute("SELECT album_id FROM albums WHERE title = %s AND artist_id = %s", 
				   (album_name, artist_id))
		album_result = cur.fetchone()
		if not album_result:
			cur.execute("""
				INSERT INTO albums (title, artist_id, cover_image_url) 
				VALUES (%s, %s, %s) RETURNING album_id
			""", (album_name, artist_id, ''))
			album_id = cur.fetchone()[0]
		else:
			album_id = album_result[0]
		
		# Update track's album_id
		cur.execute("UPDATE tracks SET album_id = %s WHERE title = %s", 
				   (album_id, track_title))
		
		conn.commit()
		cur.close()
		
		print('Album Created Successfully')
		return True
	except Exception as ex:
		if conn:
			conn.rollback()
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occured which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)


def get_album(**kwargs):
	"""
	parameters : album_name, artist_name
	if want all the albums dont pass any argument else pass name of the album or artist of the album.
	eg:- get_album(album_name = 'devdatta')
	Kwargs : album_name or artist
	"""
	conn = None
	
	if 'album_name' in kwargs:
		try:
			conn = get_connection()
			cur = conn.cursor()
			
			# Get tracks for specific album
			cur.execute("""
				SELECT t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count,
					   a.name as artist, g.name as genre, l.name as language, al.title as album
				FROM tracks t
				LEFT JOIN track_artists ta ON t.track_id = ta.track_id
				LEFT JOIN artists a ON ta.artist_id = a.artist_id
				LEFT JOIN genres g ON t.genre_id = g.genre_id
				LEFT JOIN languages l ON t.language_id = l.language_id
				LEFT JOIN albums al ON t.album_id = al.album_id
				WHERE al.title = %s
			""", (kwargs['album_name'],))
			
			rows = cur.fetchall()
			cur.close()
			
			tracks = []
			for row in rows:
				track_dict = {
					'track_id': row[0],
					'title': row[1],
					'duration_seconds': row[2],
					'location': row[3],
					'like_count': row[4],
					'artist': row[5],
					'genre': row[6],
					'language': row[7],
					'album': row[8]
				}
				tracks.append(track_dict)
			
			return tracks if tracks else []
			
		except Exception as ex:
			messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
			
			print('Exception Occured which is of type :', ex.__class__.__name__)
			y = input('If you want to see Traceback press 1 : ')
			if y == '1':
				traceback.print_exc()
			return False
		finally:
			if conn:
				release_connection(conn)
				
	elif 'artist' in kwargs:
		try:
			conn = get_connection()
			cur = conn.cursor()
			
			# Get all albums by specific artist
			cur.execute("""
				SELECT al.album_id, al.title, al.cover_image_url, a.name as artist
				FROM albums al
				LEFT JOIN artists a ON al.artist_id = a.artist_id
				WHERE a.name = %s
			""", (kwargs['artist'],))
			
			rows = cur.fetchall()
			cur.close()
			
			if not rows:
				raise Exception('No data with the given artist found')
			
			albums = []
			for row in rows:
				album_dict = {
					'album_id': row[0],
					'album_title': row[1],
					'cover_image_url': row[2],
					'artist': row[3]
				}
				albums.append(album_dict)
			
			return albums
			
		except Exception as ex:
			messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
			
			print('Exception Occurred which is of type :', ex.__class__.__name__)
			y = input('If you want to see Traceback press 1 : ')
			if y == '1':
				traceback.print_exc()
			return False
		finally:
			if conn:
				release_connection(conn)
	else:
		try:
			conn = get_connection()
			cur = conn.cursor()
			
			# Get all albums
			cur.execute("""
				SELECT al.album_id, al.title, al.cover_image_url, a.name as artist
				FROM albums al
				LEFT JOIN artists a ON al.artist_id = a.artist_id
				ORDER BY al.title
			""")
			
			rows = cur.fetchall()
			cur.close()
			
			albums = []
			for row in rows:
				album_dict = {
					'album_id': row[0],
					'album_title': row[1],
					'cover_image_url': row[2],
					'artist': row[3]
				}
				albums.append(album_dict)
			
			return albums
			
		except Exception as ex:
			messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
			
			print('Exception Occurred which is of type :', ex.__class__.__name__)
			y = input('If you want to see Traceback press 1 : ')
			if y == '1':
				traceback.print_exc()
			return False
		finally:
			if conn:
				release_connection(conn)


def get_all_tracks():
	"""
	Returns a list of all track objects
	if failed returns a false
	"""
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		cur.execute("""
			SELECT t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count,
				   a.name as artist, g.name as genre, l.name as language, al.title as album
			FROM tracks t
			LEFT JOIN track_artists ta ON t.track_id = ta.track_id
			LEFT JOIN artists a ON ta.artist_id = a.artist_id
			LEFT JOIN genres g ON t.genre_id = g.genre_id
			LEFT JOIN languages l ON t.language_id = l.language_id
			LEFT JOIN albums al ON t.album_id = al.album_id
			ORDER BY t.title
		""")
		rows = cur.fetchall()
		cur.close()
		
		tracks = []
		for row in rows:
			track_dict = {
				'track_id': row[0],
				'title': row[1],
				'duration_seconds': row[2],
				'location': row[3],
				'like_count': row[4],
				'artist': row[5],
				'genre': row[6],
				'language': row[7],
				'album': row[8]
			}
			tracks.append(track_dict)
		
		return tracks
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)
def set_genre(genre):
	'''
	:param genre:
	This is the name of the genre

	:return:
	Bool if success
	'''
	conn = None
	try:
		if(Check_genre(genre)):
			pass
		else : 
			conn = get_connection()
			cur = conn.cursor()
			cur.execute("INSERT INTO genres (name, image_url) VALUES (%s, %s)", (genre, ''))
			conn.commit()
			cur.close()
		return True
	except Exception as ex:
		if conn:
			conn.rollback()
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)
def get_tracks_by_genre(**kwargs):
	"""
	Returns a list of songs with particular genre
	kwarg : genre = 'required genre'
	else return the list of all genres
	if failed returns false
	"""
	if 'genre' in kwargs:
		conn = None
		try:
			conn = get_connection()
			cur = conn.cursor()
			cur.execute("""
				SELECT t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count,
					   a.name as artist, g.name as genre, l.name as language, al.title as album
				FROM tracks t
				LEFT JOIN track_artists ta ON t.track_id = ta.track_id
				LEFT JOIN artists a ON ta.artist_id = a.artist_id
				LEFT JOIN genres g ON t.genre_id = g.genre_id
				LEFT JOIN languages l ON t.language_id = l.language_id
				LEFT JOIN albums al ON t.album_id = al.album_id
				WHERE g.name = %s
				ORDER BY t.title
			""", (kwargs['genre'],))
			rows = cur.fetchall()
			cur.close()
			
			tracks = []
			for row in rows:
				track_dict = {
					'track_id': row[0],
					'title': row[1],
					'duration_seconds': row[2],
					'location': row[3],
					'like_count': row[4],
					'artist': row[5],
					'genre': row[6],
					'language': row[7],
					'album': row[8]
				}
				tracks.append(track_dict)
			
			return tracks
		except Exception as ex:
			messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
			print('Exception Occurred which is of type :', ex.__class__.__name__)
			y = input('If you want to see Traceback press 1 : ')
			if y == '1':
				traceback.print_exc()
			return []
		finally:
			if conn:
				release_connection(conn)
	else:
		try:
			# Truy vấn bảng genres của PostgreSQL
			conn = get_connection()
			if not conn:
				return []
			
			cur = conn.cursor()
			cur.execute("SELECT name, image_url FROM genres")
			rows = cur.fetchall()
			cur.close()
			conn.close()
			
			all_dicts = []
			for row in rows:
				my_dict = {
					'text': row[0],  # tên thể loại
					'url': row[1],   # hình ảnh thể loại
				}
				all_dicts.append(my_dict)
			return all_dicts
		except Exception as ex:
			messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
			
			print('Exception Occurred which is of type :', ex.__class__.__name__)
			y = input('If you want to see Traceback press 1 : ')
			if y == '1':
				traceback.print_exc()
			return []


def get_user(uid):
	"""
	Returns a user object that is dictionary
	of the user with attributes:
	display_name , email , password, phone_number
	"""
	# [BẮT ĐẦU get_user]
	import os
	conn = get_connection()
	if not conn:
		return False
	
	try:
		cur = conn.cursor()
		cur.execute("""
			SELECT user_id, display_name, email, password_hash, created_at
			FROM users WHERE user_id = %s
		""", (uid,))
		row = cur.fetchone()
		cur.close()
		
		if row:
			print('Successfully fetched user data: {0}'.format(row[0]))
			return {
				'uid': str(row[0]),
				'user_id': str(row[0]),
				'display_name': row[1],
				'email': row[2],
				'password_hash': row[3],
				'created_at': row[4]
			}
		else:
			# Không tìm thấy người dùng - xóa file user và trả về False
			if os.path.exists('user'):
				os.remove('user')
				print('User file deleted - user not found in database')
			return False
			
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		release_connection(conn)

	# [KẾT THÚC get_user]


def get_user_by_email(email):
	"""
	Returns a user object that is dictionary
	of the user with attributes:
	display_name , email , password, phone_number
	"""
	conn = get_connection()
	if not conn:
		return False
	
	try:
		cur = conn.cursor()
		cur.execute("""
			SELECT user_id, display_name, email, password_hash, created_at
			FROM users WHERE email = %s
		""", (email,))
		row = cur.fetchone()
		cur.close()
		
		if row:
			return {
				'uid': str(row[0]),
				'user_id': str(row[0]),
				'display_name': row[1],
				'email': row[2],
				'password_hash': row[3],
				'created_at': row[4]
			}
		else:
			from Pages.UserAuthentication.Exceptions import User_not_Found
			User_not_Found()
			return False
			
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		print(str(ex))
		return False
	finally:
		release_connection(conn)


def get_user_by_phone_number(phone):
	"""
	Returns a user object that is dictionary
	of the user with attributes:
	display_name , email , password, phone_number
	
	NOTE: phone_number column was removed from the new schema.
	This function now always returns False.
	"""
	# Phone number authentication was removed in the new schema
	# Return False to indicate user not found
	return False


def sign_in_with_email_and_password(email, password):
	"""
	Returns user if email and password match
	else false
	"""
	import hashlib

	try:
		# Lấy user từ database
		doc = get_user_by_email(email)
		
		if not doc:
			from Pages.UserAuthentication.Exceptions import User_not_Found
			User_not_Found()
			return False
		
		# Hash password để so sánh
		hashed_password = hashlib.sha256(password.encode()).hexdigest()
		
		# doc là dict, sử dụng dict keys
		if doc['email'] == email and doc['password_hash'] == hashed_password:
			# Lưu thông tin user vào session thay vì file
			from user_session import UserSession
			UserSession.set_user(doc)
			return doc
		else:
			from Pages.UserAuthentication.Exceptions import Invalid_credentials
			Invalid_credentials()
			return False
			
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		print(str(ex))
		return False


def sign_out():
	"""

	returns True
	if signed out else false
	also remove the user files

	"""
	import os
	try:
		os.remove("user")
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occured which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False

	# sign_out()
# myuser = register_user('devdatta','dkhoche70@gmail.com','9145253235','15412342')
def generate_password(uid):
	import random
	import string

	
	letters = string.ascii_lowercase
	password = ''.join(random.choice(letters) for i in range(10))
	doc_ref = db.collection(u'users').document(uid)
	doc_ref.update({
			'password'  :  password
		})
	return password



def Forget_password_email(email):
	'''

	:param otp:
		   email: email of the user
	:return: bool


	'''
	try:
		import smtplib
		
		user = get_user_by_email(email)
		if not user:
			from Pages.UserAuthentication.Exceptions import User_not_Found
			User_not_Found()
			return False
			
		password = generate_password(user['uid'])
		fromaddr = 'amplifyteam1234@gmail.com.'
		toaddrs = email
		Text = f"Hello {user['display_name']},\nThis is your new password now on.\nYour new password is {password}.\nMake sure you don't forget it.\nThanks,\nYour AmplifyTeam"
		subject = 'New Password Request'
		username = 'amplifyteam1234@gmail.com'
		smtp_password = '15412342'
		# print('i ma in the funtion')
		message = 'Subject: {}\n\n{}'.format(subject, Text)
		message = message.encode()
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(username, smtp_password)
		server.sendmail(fromaddr, toaddrs, message)
		server.quit()
		return True
	# except firebase_admin._auth_utils.UserNotFoundError as ex:
	#     from Pages.UserAuthentication.Exceptions import User_not_Found
	#     User_not_Found()
	#     return False
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False

def user_create_playlist(uid, playlist_name):
	'''


	:param uid: Unique Identification of the user which is saved in the user file in the root directory
	:param playlist_name: Name of the playlist to be created
	:return: Bool;
	'''
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		# Get user_id from uid (assuming uid is user_id for now, but we might need to map it)
		user_id = uid  # In the new schema, uid is actually user_id
		
		cur.execute("""
			INSERT INTO playlists (name, user_id) 
			VALUES (%s, %s)
		""", (playlist_name, user_id))
		
		conn.commit()
		cur.close()
		
		print('playlist created successfully')
		return True
	except Exception as ex:
		if conn:
			conn.rollback()
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)
def add_song_to_playlist(uid,playlist_name,track_name):
	'''
	:param uid: unique identification of the user
	:param playlist_name: name of a particular playlist
	:param track_name: track_title which is to be added
	:return: bool
	'''
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		# Get playlist_id from name and user_id
		cur.execute("SELECT playlist_id FROM playlists WHERE name = %s AND user_id = %s", 
				   (playlist_name, uid))
		playlist_result = cur.fetchone()
		
		if not playlist_result:
			print('Playlist not found')
			return False
		
		playlist_id = playlist_result[0]
		
		# Get track_id from track_name
		cur.execute("SELECT track_id FROM tracks WHERE title = %s", (track_name,))
		track_result = cur.fetchone()
		
		if not track_result:
			print('Track not found')
			return False
		
		track_id = track_result[0]
		
		# Get max track_order for this playlist
		cur.execute("SELECT COALESCE(MAX(track_order), 0) FROM playlist_tracks WHERE playlist_id = %s", 
				   (playlist_id,))
		max_order = cur.fetchone()[0]
		
		# Insert into playlist_tracks
		cur.execute("""
			INSERT INTO playlist_tracks (playlist_id, track_id, track_order, added_at)
			VALUES (%s, %s, %s, NOW())
			ON CONFLICT (playlist_id, track_id) DO NOTHING
		""", (playlist_id, track_id, max_order + 1))
		
		conn.commit()
		cur.close()
		
		print('Track added to playlist successfully')
		return True
	except Exception as ex:
		if conn:
			conn.rollback()
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occured which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)

def get_playlists(uid,**kwargs):
	'''
	:param uid: unique identification of the user
	:param kwargs: playlist = 'required Playlist name'
	:return: if mentioned playlist as kwarg then return a list of the all tracks of the particular playlist.
			elseif no kwarg is passed gives the names of all the playlist
			else returns false
			If there are no songs then returns a empty list
	'''
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		if 'playlist' in kwargs:
			# Get tracks for specific playlist
			cur.execute("""
				SELECT t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count,
					   a.name as artist, g.name as genre, l.name as language, al.title as album
				FROM playlist_tracks pt
				JOIN tracks t ON pt.track_id = t.track_id
				JOIN playlists pl ON pt.playlist_id = pl.playlist_id
				LEFT JOIN track_artists ta ON t.track_id = ta.track_id
				LEFT JOIN artists a ON ta.artist_id = a.artist_id
				LEFT JOIN genres g ON t.genre_id = g.genre_id
				LEFT JOIN languages l ON t.language_id = l.language_id
				LEFT JOIN albums al ON t.album_id = al.album_id
				WHERE pl.name = %s AND pl.user_id = %s
				ORDER BY pt.track_order
			""", (kwargs['playlist'], uid))
			
			rows = cur.fetchall()
			cur.close()
			
			tracks = []
			for row in rows:
				track_dict = {
					'track_id': row[0],
					'title': row[1],
					'duration_seconds': row[2],
					'location': row[3],
					'like_count': row[4],
					'artist': row[5],
					'genre': row[6],
					'language': row[7],
					'album': row[8]
				}
				tracks.append(track_dict)
			
			return tracks
		else:
			# Get all playlists of user
			cur.execute("""
				SELECT playlist_id, name, description, cover_image_url, is_public, created_at
				FROM playlists
				WHERE user_id = %s
				ORDER BY created_at DESC
			""", (uid,))
			
			rows = cur.fetchall()
			cur.close()
			
			playlists = []
			for row in rows:
				playlist_dict = {
					'playlist_id': row[0],
					'playlist_name': row[1],
					'description': row[2],
					'cover_image_url': row[3],
					'is_public': row[4],
					'created_at': row[5]
				}
				playlists.append(playlist_dict)
			
			return playlists
			
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occured which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)

def Following_artist(artist_name,uid):
	'''

	params : artist_name : The name of the artisit which is to be followed
		   : uid : unique Identification No. of the user
	return artist name

	'''
	try:
		collection = db.collection(u'users/'+uid+'/Following_Artist').document(artist_name)
		collection.set({
			'name' : artist_name
		})
		return artist_name
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occured which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False

def get_user_artists(uid):
	doc_ref = db.collection(u'users/'+uid+'/Following_Artist').stream()
	object_list = list(map(lambda x: x.to_dict(), doc_ref))
	return object_list

def add_liked_songs(track_object,uid):
	'''

	params : track_object : The object of the track
		   : uid : unique Identification No. of the user
	return Bool

	'''
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		# First get the track_id from the track title
		cur.execute("SELECT track_id FROM tracks WHERE title = %s", (track_object['title'],))
		track_row = cur.fetchone()
		
		if track_row:
			track_id = track_row[0]
			# Insert into user_liked_songs table
			cur.execute("""
				INSERT INTO user_liked_songs (user_id, track_id, liked_at)
				VALUES (%s, %s, NOW())
				ON CONFLICT (user_id, track_id) DO NOTHING
			""", (uid, track_id))
			
			conn.commit()
			cur.close()
			
			# Update like count
			add_like_count(track_object['title'])
			print('Added Liked song')
			return True
		else:
			print('Track not found')
			return False
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)

def delete_liked_song(uid,track_title):
	'''

	params : track title : The title of the track to be deleted
		   : uid : unique Identification No. of the user
	return Bool

	'''
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		# First get the track_id from the track title
		cur.execute("SELECT track_id FROM tracks WHERE title = %s", (track_title,))
		track_row = cur.fetchone()
		
		if track_row:
			track_id = track_row[0]
			# Delete from user_liked_songs table
			cur.execute("""
				DELETE FROM user_liked_songs WHERE user_id = %s AND track_id = %s
			""", (uid, track_id))
			
			conn.commit()
			cur.close()
			
			# Update like count
			decrease_like_count(track_title)
			print('deleted Liked song')
			return True
		else:
			print('Track not found')
			return False
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)

def get_all_liked_songs(uid): 
	try:
		# Truy vấn bảng user_liked_songs cho các bài hát đã thích của người dùng này
		conn = get_connection()
		cur = conn.cursor()
		cur.execute("""
			SELECT t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count,
			       a.name as artist, g.name as genre, l.name as language, al.title as album
			FROM user_liked_songs ul
			JOIN tracks t ON ul.track_id = t.track_id
			LEFT JOIN track_artists ta ON t.track_id = ta.track_id
			LEFT JOIN artists a ON ta.artist_id = a.artist_id
			LEFT JOIN genres g ON t.genre_id = g.genre_id
			LEFT JOIN languages l ON t.language_id = l.language_id
			LEFT JOIN albums al ON t.album_id = al.album_id
			WHERE ul.user_id = %s
			ORDER BY ul.liked_at DESC
		""", (uid,))
		
		rows = cur.fetchall()
		cur.close()
		conn.close()
		
		# Chuyển đổi sang định dạng dict để tương thích với cấu trúc Firebase
		liked_songs = []
		for row in rows:
			liked_songs.append({
				'track_id': row[0],
				'title': row[1],
				'duration_seconds': row[2],
				'location': row[3],
				'like_count': row[4],
				'artist': row[5],
				'genre': row[6],
				'language': row[7],
				'album': row[8]
			})
		
		return liked_songs
		
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occured which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return []


	
def add_language_and_Like_count():
	'''

	Never use this function once used.
	Used only when all songs are of same language

	'''
	my_objects = get_all_tracks()
	for i in my_objects:
		doc_ref = db.collection(u'Tracks').document(i['title'])
		doc_ref.update({
			'like_count': 0,
			'Language': 'English'
		})
		doc_ref_artist = db.collection(u'artist/'+i['artist']+'/tracks').document(i['title'])
		doc_ref_artist.update({
			'like_count': 0,
			'Language': 'English'
		})

def order_simple_trending_song():
	'''
	Returns list of songs in the descending order

	'''
	try:
		# Truy vấn bảng tracks của PostgreSQL được sắp xếp theo like_count
		conn = get_connection()
		if not conn:
			return []
		
		cur = conn.cursor()
		cur.execute("""
			SELECT t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count,
			       a.name as artist, g.name as genre, l.name as language, al.title as album
			FROM tracks t
			LEFT JOIN track_artists ta ON t.track_id = ta.track_id
			LEFT JOIN artists a ON ta.artist_id = a.artist_id
			LEFT JOIN genres g ON t.genre_id = g.genre_id
			LEFT JOIN languages l ON t.language_id = l.language_id
			LEFT JOIN albums al ON t.album_id = al.album_id
			ORDER BY t.like_count DESC
			LIMIT 100
		""")
		rows = cur.fetchall()
		cur.close()
		conn.close()
		
		# Chuyển đổi sang định dạng dict để tương thích
		tracks = []
		for row in rows:
			tracks.append({
				'track_id': row[0],
				'title': row[1],
				'duration_seconds': row[2],
				'location': row[3],
				'like_count': row[4],
				'artist': row[5],
				'genre': row[6],
				'language': row[7],
				'album': row[8]
			})
		return tracks
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occured which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return []
		

def add_like_count(title):
	"""
	Increments the like_count for a track in PostgreSQL
	"""
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		# Update like_count in tracks table
		cur.execute("""
			UPDATE tracks 
			SET like_count = like_count + 1 
			WHERE title = %s
		""", (title,))
		
		conn.commit()
		cur.close()
		
		return True
	except Exception as ex:
		if conn:
			conn.rollback()
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occured which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)


def decrease_like_count(title):
	"""
	Decrements the like_count for a track in PostgreSQL
	"""
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		
		# Update like_count in tracks table
		cur.execute("""
			UPDATE tracks 
			SET like_count = GREATEST(like_count - 1, 0)
			WHERE title = %s
		""", (title,))
		
		conn.commit()
		cur.close()
		
		return True
	except Exception as ex:
		if conn:
			conn.rollback()
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occured which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)


def get_genre(genre_name):
	'''
	parameters: genre name
	output:return the dictionary with key genre_name ,genre_image
	'''
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		cur.execute("""
			SELECT name, image_url FROM genres WHERE name = %s
		""", (genre_name,))
		row = cur.fetchone()
		cur.close()
		
		if row:
			return {
				'genre_name': row[0],
				'genre_image': row[1]
			}
		else:
			return False
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occurred which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)

def get_artist(artist_name):
	'''
	parameters: artist name
	output:return the dictionary with key name ,image_url
	'''
	conn = None
	try:
		conn = get_connection()
		cur = conn.cursor()
		cur.execute("""
			SELECT name, image_url FROM artists WHERE name = %s
		""", (artist_name,))
		row = cur.fetchone()
		cur.close()
		
		if row:
			return {
				'name': row[0],
				'image_url': row[1]
			}
		else:
			return False
	except Exception as ex:
		messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
		
		print('Exception Occured which is of type :', ex.__class__.__name__)
		y = input('If you want to see Traceback press 1 : ')
		if y == '1':
			traceback.print_exc()
		return False
	finally:
		if conn:
			release_connection(conn)