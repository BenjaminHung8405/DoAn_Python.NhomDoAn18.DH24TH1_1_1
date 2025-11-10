def remove_accents(text):
    """
    Remove Vietnamese accents from text for better search matching.
    """
    accents = {
        'àáảãạăằắẳẵặâầấẩẫậ': 'a',
        'ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬ': 'A',
        'èéẻẽẹêềếểễệ': 'e',
        'ÈÉẺẼẸÊỀẾỂỄỆ': 'E',
        'ìíỉĩị': 'i',
        'ÌÍỈĨỊ': 'I',
        'òóỏõọôồốổỗộơờớởỡợ': 'o',
        'ÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ': 'O',
        'ùúủũụưừứửữự': 'u',
        'ÙÚỦŨỤƯỪỨỬỮỰ': 'U',
        'ỳýỷỹỵ': 'y',
        'ỲÝỶỸỴ': 'Y',
        'đ': 'd',
        'Đ': 'D'
    }
    for accented, plain in accents.items():
        for char in accented:
            text = text.replace(char, plain)
    return text


def get_song_file_path(song_name):
    """
    Convert song name to lowercase and remove accents to create file path.
    Used for matching song files in the songs directory.
    
    Args:
        song_name (str): The original song name/title
        
    Returns:
        str: Processed song name suitable for file path matching
    """
    if not song_name:
        return ""
    
    # Remove accents first, then lowercase
    processed = remove_accents(song_name)
    return processed.lower()


def find_song_file(song_name):
    """
    Find the actual song file path by processing the song name.
    Looks for MP3 files in the songs directory that match the processed name.
    
    Args:
        song_name (str): The song name/title to search for
        
    Returns:
        str: Full path to the song file if found, None otherwise
    """
    import os
    
    if not song_name:
        return None
    
    # Get the processed name for matching
    processed_name = get_song_file_path(song_name)
    
    # Path to songs directory
    songs_dir = os.path.join(os.path.dirname(__file__), 'songs')
    
    if not os.path.exists(songs_dir):
        return None
    
    # Look for files that contain the processed name
    for filename in os.listdir(songs_dir):
        if filename.lower().endswith('.mp3'):
            # Process the filename too for comparison
            processed_filename = get_song_file_path(filename.replace('.mp3', ''))
            
            # Check if the processed names match (partial match)
            if processed_name in processed_filename or processed_filename in processed_name:
                return os.path.join(songs_dir, filename)
    
    return None