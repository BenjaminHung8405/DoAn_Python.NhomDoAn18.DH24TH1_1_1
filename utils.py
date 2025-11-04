"""
Utility functions for cross-platform compatibility
"""

import os
import logging
from PIL import Image, ImageTk

logger = logging.getLogger(__name__)

def get_image_path(filename):
    """Get cross-platform path for image files"""
    return os.path.join('images', filename)

def get_activity_path(filename):
    """Get cross-platform path for activity indicator files"""
    return os.path.join('ActivityIndicator', filename)

def load_font_file(filename):
    """Load custom font file using pyglet"""
    import pyglet
    pyglet.font.add_file(os.path.join('fonts', filename))

def load_pil_image(filename, folder='images'):
    """Load PIL Image from file. Returns Image or None on error.
    
    Args:
        filename: image filename (e.g., 'button_heart.png')
        folder: subdirectory (default 'images')
    """
    try:
        path = os.path.join(folder, filename)
        if not os.path.exists(path):
            logger.warning(f"Image file not found: {path}")
            return None
        return Image.open(path)
    except Exception as e:
        logger.error(f"Error loading PIL image {filename}: {e}")
        return None

def load_photoimage(filename, folder='images', height=None, width=None):
    """Load tk.PhotoImage from file. Returns PhotoImage or None on error.
    
    Args:
        filename: image filename (e.g., 'loading.png')
        folder: subdirectory (default 'images')
        height: optional height
        width: optional width
    """
    try:
        path = os.path.join(folder, filename)
        if not os.path.exists(path):
            logger.warning(f"Image file not found: {path}")
            return None
        
        import tkinter as tk
        kwargs = {'file': path}
        if height:
            kwargs['height'] = height
        if width:
            kwargs['width'] = width
        
        return tk.PhotoImage(**kwargs)
    except Exception as e:
        logger.error(f"Error loading PhotoImage {filename}: {e}")
        return None

def load_image_from_source(source):
    """Load image from file path or URL and return PhotoImage"""
    try:
        if source.startswith(('http://', 'https://')):
            # For URLs, you might need to download first
            # For now, assume local paths
            pass
        # Assume local file path - normalize to cross-platform
        path = source.replace('\\', os.sep).replace('/', os.sep)
        if not os.path.exists(path):
            logger.warning(f"Image file not found: {path}")
            return None
        image = Image.open(path)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        logger.error(f"Error loading image from {source}: {e}")
        return None
