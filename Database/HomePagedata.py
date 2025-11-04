from Database.Database import (
    get_tracks_by_language,
    get_all_artists,
    get_all_genres,
    get_trending_tracks
)

# Language data
language_data = get_tracks_by_language() or []

# Trending songs data
Trending_data = get_trending_tracks(limit=20)

# Artist data
artist_data = get_all_artists() or []

# Genre data  
genre_data = get_all_genres() or []
