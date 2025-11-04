-- Seed data for Amplify Music Player Database

-- Insert sample genres
INSERT INTO genres (genre_name, genre_image) VALUES
    ('Pop', 'https://via.placeholder.com/150/FF6B6B/ffffff?text=Pop'),
    ('Rock', 'https://via.placeholder.com/150/4ECDC4/ffffff?text=Rock'),
    ('Hip Hop', 'https://via.placeholder.com/150/45B7D1/ffffff?text=HipHop'),
    ('Jazz', 'https://via.placeholder.com/150/FFA07A/ffffff?text=Jazz'),
    ('Classical', 'https://via.placeholder.com/150/98D8C8/ffffff?text=Classical'),
    ('Electronic', 'https://via.placeholder.com/150/F7DC6F/ffffff?text=Electronic'),
    ('R&B', 'https://via.placeholder.com/150/BB8FCE/ffffff?text=R%26B'),
    ('Country', 'https://via.placeholder.com/150/85C1E2/ffffff?text=Country'),
    ('K-Pop', 'https://via.placeholder.com/150/F8B500/ffffff?text=K-Pop'),
    ('V-Pop', 'https://via.placeholder.com/150/ED4C67/ffffff?text=V-Pop')
ON CONFLICT (genre_name) DO NOTHING;

-- Insert sample languages
INSERT INTO languages (language_name, language_image) VALUES
    ('English', 'https://via.placeholder.com/150/3498db/ffffff?text=English'),
    ('Vietnamese', 'https://via.placeholder.com/150/e74c3c/ffffff?text=Vietnamese'),
    ('Korean', 'https://via.placeholder.com/150/2ecc71/ffffff?text=Korean'),
    ('Japanese', 'https://via.placeholder.com/150/f39c12/ffffff?text=Japanese'),
    ('Spanish', 'https://via.placeholder.com/150/9b59b6/ffffff?text=Spanish'),
    ('French', 'https://via.placeholder.com/150/1abc9c/ffffff?text=French'),
    ('Chinese', 'https://via.placeholder.com/150/e67e22/ffffff?text=Chinese'),
    ('Thai', 'https://via.placeholder.com/150/34495e/ffffff?text=Thai')
ON CONFLICT (language_name) DO NOTHING;

-- Insert sample artists
INSERT INTO artists (name, image_url) VALUES
    ('Unknown Artist', 'https://via.placeholder.com/300/95a5a6/ffffff?text=Unknown'),
    ('Various Artists', 'https://via.placeholder.com/300/7f8c8d/ffffff?text=Various'),
    ('Sơn Tùng M-TP', 'https://via.placeholder.com/300/e74c3c/ffffff?text=SonTung'),
    ('BLACKPINK', 'https://via.placeholder.com/300/f39c12/ffffff?text=BLACKPINK'),
    ('BTS', 'https://via.placeholder.com/300/9b59b6/ffffff?text=BTS'),
    ('Taylor Swift', 'https://via.placeholder.com/300/3498db/ffffff?text=TaylorSwift'),
    ('Ed Sheeran', 'https://via.placeholder.com/300/2ecc71/ffffff?text=EdSheeran'),
    ('The Weeknd', 'https://via.placeholder.com/300/e67e22/ffffff?text=TheWeeknd'),
    ('Adele', 'https://via.placeholder.com/300/1abc9c/ffffff?text=Adele'),
    ('Drake', 'https://via.placeholder.com/300/34495e/ffffff?text=Drake')
ON CONFLICT (name) DO NOTHING;

-- Insert sample tracks
INSERT INTO tracks (title, artist, genre, location, language, like_count) VALUES
    ('Lạc Trôi', 'Sơn Tùng M-TP', 'V-Pop', 'https://example.com/music/lac-troi.mp3', 'Vietnamese', 1250),
    ('Nơi Này Có Anh', 'Sơn Tùng M-TP', 'V-Pop', 'https://example.com/music/noi-nay-co-anh.mp3', 'Vietnamese', 980),
    ('Pink Venom', 'BLACKPINK', 'K-Pop', 'https://example.com/music/pink-venom.mp3', 'Korean', 2340),
    ('Shut Down', 'BLACKPINK', 'K-Pop', 'https://example.com/music/shut-down.mp3', 'Korean', 1890),
    ('Dynamite', 'BTS', 'K-Pop', 'https://example.com/music/dynamite.mp3', 'Korean', 3450),
    ('Butter', 'BTS', 'K-Pop', 'https://example.com/music/butter.mp3', 'English', 3120),
    ('Anti-Hero', 'Taylor Swift', 'Pop', 'https://example.com/music/anti-hero.mp3', 'English', 2780),
    ('Shake It Off', 'Taylor Swift', 'Pop', 'https://example.com/music/shake-it-off.mp3', 'English', 2450),
    ('Shape of You', 'Ed Sheeran', 'Pop', 'https://example.com/music/shape-of-you.mp3', 'English', 3890),
    ('Perfect', 'Ed Sheeran', 'Pop', 'https://example.com/music/perfect.mp3', 'English', 3210),
    ('Blinding Lights', 'The Weeknd', 'Pop', 'https://example.com/music/blinding-lights.mp3', 'English', 4560),
    ('Starboy', 'The Weeknd', 'R&B', 'https://example.com/music/starboy.mp3', 'English', 2890),
    ('Someone Like You', 'Adele', 'Pop', 'https://example.com/music/someone-like-you.mp3', 'English', 3670),
    ('Rolling in the Deep', 'Adele', 'Pop', 'https://example.com/music/rolling-in-the-deep.mp3', 'English', 3340),
    ('One Dance', 'Drake', 'Hip Hop', 'https://example.com/music/one-dance.mp3', 'English', 2910),
    ('Gods Plan', 'Drake', 'Hip Hop', 'https://example.com/music/gods-plan.mp3', 'English', 2670),
    ('Sample Track 1', 'Unknown Artist', 'Pop', 'https://example.com/music/sample1.mp3', 'English', 145),
    ('Sample Track 2', 'Unknown Artist', 'Rock', 'https://example.com/music/sample2.mp3', 'English', 234),
    ('Sample Track 3', 'Various Artists', 'Jazz', 'https://example.com/music/sample3.mp3', 'English', 189),
    ('Sample Track 4', 'Various Artists', 'Electronic', 'https://example.com/music/sample4.mp3', 'English', 276)
ON CONFLICT (title, artist) DO NOTHING;

-- Note: Update the 'location' URLs with actual music file URLs or local paths
-- For testing, you can use public domain music or sample files
