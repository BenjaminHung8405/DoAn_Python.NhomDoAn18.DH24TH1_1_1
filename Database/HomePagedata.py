import traceback

from Database.config import db


def get_artist_row():
    try:
        from Database.config import get_connection, release_connection
        conn = get_connection()
        if not conn:
            return False
        
        cur = conn.cursor()
        cur.execute("SELECT artist_id, name, image_url FROM artists ORDER BY name")
        rows = cur.fetchall()
        cur.close()
        release_connection(conn)
        
        artists = []
        for row in rows:
            artist_dict = {
                'artist_id': row[0],
                'name': row[1],
                'image_url': row[2] if row[2] else ''
            }
            artists.append(artist_dict)
        return artists
    except Exception as ex:
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def get_artist_data():
    data = get_artist_row()
    from Database.Database import get_artist_tracks
    my_data = list(map(lambda x: get_artist_tracks(x['name']), data))
    artist_data = []
    for i in range(len(data)):
        my_dict = {
            'text': data[i]['name'],
            'url': data[i]['image_url'],
            'tracks': my_data[i]
        }

        artist_data.append(my_dict)

    return artist_data


def get_genre_data():
    from Database.Database import get_tracks_by_genre
    genre_data = get_tracks_by_genre()

    tracks_list = []
    for i in range(len(genre_data)):
        my_tracks = get_tracks_by_genre(genre=genre_data[i]['text'])
        genre_data[i]['tracks'] = my_tracks
    return genre_data

def get_language_data():
    from Database.Database import get_tracks_by_language
    language_data = get_tracks_by_language()

    tracks_list = []
    for i in range(len(language_data)):
        my_tracks = get_tracks_by_language(language=language_data[i]['text'])
        language_data[i]['tracks'] = my_tracks
    return language_data

def Top_hits_data():
    from Database.Database import  order_simple_trending_song
    data = order_simple_trending_song()
    my_dict = {
        'text':'Bài hát thịnh hành',
        'url':'https://firebasestorage.googleapis.com/v0/b/another-tk-player.appspot.com/o/Top%20Hits.jpg?alt=media&token=38eec66b-9bf9-455c-b24f-d8cdf6906186',
        'tracks':data
    }
    my_list = []
    my_list.append(my_dict)
    return my_list

def get_album_data():
    """Get all albums from database for homepage display"""
    try:
        from Database.config import get_connection, release_connection
        from Database.Database import get_album
        
        # Get all albums
        albums = get_album()
        if not albums:
            return []
        
        album_data = []
        for album in albums:
            # Get tracks for this album
            tracks = get_album(album_name=album['album_title'])
            
            album_dict = {
                'album_id': album['album_id'],
                'text': album['album_title'],
                'url': album.get('cover_image_url', ''),  # Fixed: use cover_image_url from schema
                'tracks': tracks if tracks else []
            }
            album_data.append(album_dict)
        
        return album_data
    except Exception as ex:
        print(f'Error loading album data: {ex}')
        import traceback
        traceback.print_exc()
        return []

def get_playlist_data():
    """Get featured/public playlists for homepage display"""
    try:
        from Database.config import get_connection, release_connection
        
        conn = get_connection()
        if not conn:
            return []
        
        cur = conn.cursor()
        # Get playlists (you can filter for public/featured playlists)
        cur.execute("""
            SELECT p.playlist_id, p.name, p.description, p.cover_image_url,
                   u.display_name as creator_name
            FROM playlists p
            LEFT JOIN users u ON p.user_id = u.user_id
            WHERE p.is_public = TRUE
            ORDER BY p.created_at DESC
            LIMIT 20
        """)
        
        rows = cur.fetchall()
        
        playlist_data = []
        for row in rows:
            playlist_id = row[0]
            
            # Get tracks for this playlist (using track_order from schema)
            cur.execute("""
                SELECT t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count,
                       STRING_AGG(a.name, ', ') as artist, g.name as genre, l.name as language, al.title as album, pt.track_order
                FROM playlist_tracks pt
                JOIN tracks t ON pt.track_id = t.track_id
                LEFT JOIN track_artists ta ON t.track_id = ta.track_id
                LEFT JOIN artists a ON ta.artist_id = a.artist_id
                LEFT JOIN genres g ON t.genre_id = g.genre_id
                LEFT JOIN languages l ON t.language_id = l.language_id
                LEFT JOIN albums al ON t.album_id = al.album_id
                WHERE pt.playlist_id = %s
                GROUP BY t.track_id, t.title, t.duration_seconds, t.location_url, t.like_count, g.name, l.name, al.title, pt.track_order
                ORDER BY pt.track_order
            """, (playlist_id,))
            
            track_rows = cur.fetchall()
            tracks = []
            for track_row in track_rows:
                tracks.append({
                    'track_id': track_row[0],
                    'title': track_row[1],
                    'duration_seconds': track_row[2],
                    'location': track_row[3],
                    'like_count': track_row[4],
                    'artist': track_row[5],
                    'genre': track_row[6],
                    'language': track_row[7],
                    'album': track_row[8]
                })
            
            playlist_dict = {
                'text': row[1],  # playlist name
                'url': row[3] if row[3] else '',  # cover image
                'tracks': tracks
            }
            playlist_data.append(playlist_dict)
        
        cur.close()
        release_connection(conn)
        return playlist_data
        
    except Exception as ex:
        print(f'Error loading playlist data: {ex}')
        import traceback
        traceback.print_exc()
        return []

genre_data = get_genre_data()
artist_data = get_artist_data()
language_data = get_language_data()
Trending_data = Top_hits_data()
album_data = get_album_data()
playlist_data = get_playlist_data()
