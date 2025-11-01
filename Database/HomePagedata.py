from Database.Database import execute_query


def get_data():
    """Get real data from PostgreSQL database for HomePage"""
    
    sections = []
    
    # 1. Popular Albums (Albums có nhiều tracks nhất)
    popular_albums = get_popular_albums()
    if popular_albums:
        sections.append({
            'name': 'Popular Albums',
            'data': popular_albums
        })
    
    # 2. Trending Tracks (Tracks có like_count cao nhất)
    trending_tracks = get_trending_tracks()
    if trending_tracks:
        sections.append({
            'name': 'Trending Now',
            'data': trending_tracks
        })
    
    # 3. Top Artists (Artists có nhiều tracks nhất)
    top_artists = get_top_artists()
    if top_artists:
        sections.append({
            'name': 'Top Artists',
            'data': top_artists
        })
    
    # 4. Recent Albums
    recent_albums = get_recent_albums()
    if recent_albums:
        sections.append({
            'name': 'Recently Added',
            'data': recent_albums
        })
    
    # Fallback to mock data if database is empty
    if not sections:
        return get_mock_data()
    
    return sections


def get_popular_albums(limit=10):
    """Get popular albums with their tracks"""
    query = """
        SELECT 
            a.album_id,
            a.title,
            a.cover_image_url,
            COUNT(t.track_id) as track_count
        FROM albums a
        LEFT JOIN tracks t ON a.album_id = t.album_id
        GROUP BY a.album_id, a.title, a.cover_image_url
        HAVING COUNT(t.track_id) > 0
        ORDER BY track_count DESC
        LIMIT %s
    """
    
    results = execute_query(query, (limit,))
    if not results:
        return []
    
    albums = []
    for row in results:
        album_id, title, cover_url, _ = row
        tracks = get_album_tracks(album_id)
        
        albums.append({
            'text': title,
            'url': cover_url or 'https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art.png',
            'tracks': tracks,
            'album_id': album_id
        })
    
    return albums


def get_trending_tracks(limit=10):
    """Get trending tracks grouped by album/artist"""
    query = """
        SELECT 
            t.track_id,
            t.title,
            t.duration_seconds,
            t.like_count,
            a.title as album_title,
            a.cover_image_url,
            ar.name as artist_name
        FROM tracks t
        LEFT JOIN albums a ON t.album_id = a.album_id
        LEFT JOIN track_artists ta ON t.track_id = ta.track_id
        LEFT JOIN artists ar ON ta.artist_id = ar.artist_id
        ORDER BY t.like_count DESC
        LIMIT %s
    """
    
    results = execute_query(query, (limit,))
    if not results:
        return []
    
    items = []
    for row in results:
        track_id, title, duration, likes, album_title, cover_url, artist_name = row
        
        items.append({
            'text': f"{title} - {artist_name or 'Unknown'}",
            'url': cover_url or 'https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art.png',
            'tracks': [{
                'title': title,
                'artist': artist_name or 'Unknown Artist',
                'duration': format_duration(duration)
            }],
            'track_id': track_id
        })
    
    return items


def get_top_artists(limit=10):
    """Get top artists by track count"""
    query = """
        SELECT 
            ar.artist_id,
            ar.name,
            ar.image_url,
            COUNT(ta.track_id) as track_count
        FROM artists ar
        LEFT JOIN track_artists ta ON ar.artist_id = ta.artist_id
        GROUP BY ar.artist_id, ar.name, ar.image_url
        HAVING COUNT(ta.track_id) > 0
        ORDER BY track_count DESC
        LIMIT %s
    """
    
    results = execute_query(query, (limit,))
    if not results:
        return []
    
    artists = []
    for row in results:
        artist_id, name, image_url, _ = row
        tracks = get_artist_tracks(artist_id)
        
        artists.append({
            'text': name,
            'url': image_url or 'https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art.png',
            'tracks': tracks,
            'artist_id': artist_id
        })
    
    return artists


def get_recent_albums(limit=10):
    """Get recently added albums"""
    query = """
        SELECT 
            a.album_id,
            a.title,
            a.cover_image_url,
            a.release_date
        FROM albums a
        WHERE EXISTS (SELECT 1 FROM tracks t WHERE t.album_id = a.album_id)
        ORDER BY a.release_date DESC
        LIMIT %s
    """
    
    results = execute_query(query, (limit,))
    if not results:
        return []
    
    albums = []
    for row in results:
        album_id, title, cover_url, _ = row
        tracks = get_album_tracks(album_id)
        
        albums.append({
            'text': title,
            'url': cover_url or 'https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art.png',
            'tracks': tracks,
            'album_id': album_id
        })
    
    return albums


def get_album_tracks(album_id):
    """Get all tracks from an album"""
    query = """
        SELECT 
            t.title,
            t.duration_seconds,
            ar.name as artist_name
        FROM tracks t
        LEFT JOIN track_artists ta ON t.track_id = ta.track_id
        LEFT JOIN artists ar ON ta.artist_id = ar.artist_id
        WHERE t.album_id = %s
        ORDER BY t.track_id
    """
    
    results = execute_query(query, (album_id,))
    if not results:
        return []
    
    tracks = []
    for row in results:
        title, duration, artist_name = row
        tracks.append({
            'title': title,
            'artist': artist_name or 'Unknown Artist',
            'duration': format_duration(duration)
        })
    
    return tracks


def get_artist_tracks(artist_id, limit=10):
    """Get tracks by an artist"""
    query = """
        SELECT 
            t.title,
            t.duration_seconds,
            ar.name as artist_name
        FROM tracks t
        JOIN track_artists ta ON t.track_id = ta.track_id
        JOIN artists ar ON ta.artist_id = ar.artist_id
        WHERE ar.artist_id = %s
        ORDER BY t.like_count DESC
        LIMIT %s
    """
    
    results = execute_query(query, (artist_id, limit))
    if not results:
        return []
    
    tracks = []
    for row in results:
        title, duration, artist_name = row
        tracks.append({
            'title': title,
            'artist': artist_name,
            'duration': format_duration(duration)
        })
    
    return tracks


def format_duration(seconds):
    """Convert seconds to MM:SS format"""
    if not seconds:
        return "0:00"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def get_mock_data():
    """Fallback mock data if database is empty"""
    return [
        {
            'name': 'Popular Albums',
            'data': [
                {
                    'text': 'Sample Album',
                    'url': 'https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art.png',
                    'tracks': [
                        {'title': 'Sample Song', 'artist': 'Sample Artist', 'duration': '3:45'}
                    ]
                }
            ]
        }
    ]