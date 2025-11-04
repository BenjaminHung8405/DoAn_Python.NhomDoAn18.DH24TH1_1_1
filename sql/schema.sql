-- Schema for Amplify Music Player Database (PostgreSQL)

-- Users table (already exists based on provided schema)
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    display_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    phone_number VARCHAR(20)
);

-- Artists table
CREATE TABLE IF NOT EXISTS artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Genres table
CREATE TABLE IF NOT EXISTS genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(100) UNIQUE NOT NULL,
    genre_image TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Languages table
CREATE TABLE IF NOT EXISTS languages (
    language_id SERIAL PRIMARY KEY,
    language_name VARCHAR(100) UNIQUE NOT NULL,
    language_image TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tracks table
CREATE TABLE IF NOT EXISTS tracks (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    location TEXT NOT NULL, -- URL or file path to the music file
    language VARCHAR(100),
    like_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(title, artist)
);

-- User liked tracks table (for tracking user likes)
CREATE TABLE IF NOT EXISTS user_liked_tracks (
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    track_id INTEGER REFERENCES tracks(track_id) ON DELETE CASCADE,
    liked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, track_id)
);

-- Playlists table
CREATE TABLE IF NOT EXISTS playlists (
    playlist_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Playlist tracks table
CREATE TABLE IF NOT EXISTS playlist_tracks (
    playlist_id INTEGER REFERENCES playlists(playlist_id) ON DELETE CASCADE,
    track_id INTEGER REFERENCES tracks(track_id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, track_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_tracks_artist ON tracks(artist);
CREATE INDEX IF NOT EXISTS idx_tracks_genre ON tracks(genre);
CREATE INDEX IF NOT EXISTS idx_tracks_language ON tracks(language);
CREATE INDEX IF NOT EXISTS idx_tracks_like_count ON tracks(like_count DESC);
CREATE INDEX IF NOT EXISTS idx_user_liked_tracks_user ON user_liked_tracks(user_id);
CREATE INDEX IF NOT EXISTS idx_playlists_user ON playlists(user_id);

-- Insert sample data for genres
INSERT INTO genres (genre_name, genre_image) VALUES
    ('Pop', ''),
    ('Rock', ''),
    ('Hip Hop', ''),
    ('Jazz', ''),
    ('Classical', ''),
    ('Electronic', ''),
    ('R&B', ''),
    ('Country', '')
ON CONFLICT (genre_name) DO NOTHING;

-- Insert sample data for languages
INSERT INTO languages (language_name, language_image) VALUES
    ('English', ''),
    ('Vietnamese', ''),
    ('Korean', ''),
    ('Japanese', ''),
    ('Spanish', ''),
    ('French', '')
ON CONFLICT (language_name) DO NOTHING;

-- Insert sample artists
INSERT INTO artists (name, image_url) VALUES
    ('Unknown Artist', ''),
    ('Various Artists', '')
ON CONFLICT (name) DO NOTHING;
