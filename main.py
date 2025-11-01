import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

from Base import top
from Base.bottom import Bottom
from Base.sidebar import Sidebar
from ActivityIndicator.Activity_Indicator import ImageLabel
from Pages.Resource.HorizontalScrollableFrame import HorizontalScrollableFrame
import requests
from io import BytesIO
import pyglet
import threading
import time
from pathlib import Path
import hashlib


# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Global cache for loaded images
IMAGE_CACHE = {}
CACHE_DIR = Path("cache/images")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def wid():
    global w
    return w


def hei():
    global height
    return height


def num():
    global number
    return number


def resize_and_crop(image, size):
    """
    Resize image to fill the size, cropping the excess to maintain aspect ratio
    Similar to CSS: background-size: cover
    
    Args:
        image: PIL Image object
        size: tuple (width, height)
    
    Returns:
        PIL Image object
    """
    img = image.copy()
    img_ratio = img.width / img.height
    target_ratio = size[0] / size[1]
    
    if img_ratio > target_ratio:
        # Image is wider than target - fit height and crop width
        new_height = size[1]
        new_width = int(new_height * img_ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Crop from center
        left = (new_width - size[0]) // 2
        img = img.crop((left, 0, left + size[0], size[1]))
    else:
        # Image is taller than target - fit width and crop height
        new_width = size[0]
        new_height = int(new_width / img_ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Crop from center
        top = (new_height - size[1]) // 2
        img = img.crop((0, top, size[0], top + size[1]))
    
    return img


def get_cache_path(url):
    """Get cache file path for a URL"""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return CACHE_DIR / f"{url_hash}.png"


def load_from_cache(url):
    """Try to load image from cache"""
    cache_path = get_cache_path(url)
    if cache_path.exists():
        try:
            return Image.open(cache_path)
        except Exception as e:
            print(f"Cache read error: {e}")
            cache_path.unlink(missing_ok=True)
    return None


def save_to_cache(url, image):
    """Save image to cache"""
    try:
        cache_path = get_cache_path(url)
        image.save(cache_path, "PNG")
    except Exception as e:
        print(f"Cache write error: {e}")


def load_image_from_url(url, size=(300, 300), max_retries=3):
    """
    Load image from URL with retry logic and caching
    Returns PIL Image object with aspect ratio preserved
    """
    # Check memory cache first
    if url in IMAGE_CACHE:
        return IMAGE_CACHE[url].copy()
    
    # Check disk cache
    cached_img = load_from_cache(url)
    if cached_img:
        img = resize_and_crop(cached_img, size)
        IMAGE_CACHE[url] = img
        return img.copy()
    
    # Download with retry
    for attempt in range(max_retries):
        try:
            # Set headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Increase timeout and use stream
            timeout = 15 + (attempt * 5)  # Increase timeout on retries
            response = requests.get(url, headers=headers, timeout=timeout, stream=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type.lower():
                print(f"Warning: URL returned {content_type}, not an image: {url}")
                break
            
            # Load image
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (40, 40, 40))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to cache before resizing
            save_to_cache(url, img)
            
            # Resize and crop to maintain aspect ratio
            img = resize_and_crop(img, size)
            
            # Cache in memory
            IMAGE_CACHE[url] = img
            
            return img.copy()
            
        except requests.exceptions.Timeout:
            print(f"Timeout loading image (attempt {attempt + 1}/{max_retries}): {url}")
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
            continue
            
        except requests.exceptions.RequestException as e:
            print(f"Network error loading image (attempt {attempt + 1}/{max_retries}): {url} - {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
            continue
            
        except Exception as e:
            print(f"Error loading image from {url}: {e}")
            break
    
    # All retries failed, return placeholder
    return create_placeholder_image(size)


def create_placeholder_image(size=(300, 300), text="No Image"):
    """Create a placeholder image with text"""
    img = Image.new('RGB', size, color='#282828')
    draw = ImageDraw.Draw(img)
    
    # Calculate text position (centered)
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = None
    
    # Get text bounding box
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width = len(text) * 6
        text_height = 10
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill='#666666', font=font)
    
    return img


class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Splash")
        self['bg'] = '#000000'
        self.overrideredirect(True)
        
        # Main container
        container = tk.Frame(self, bg='#000000')
        container.pack(fill="both", expand=True)
        
        # Loading animation
        try:
            lbl = ImageLabel(container)
            lbl['bd'] = 0
            lbl['bg'] = '#000000'
            lbl.pack(pady=(100, 20))
            lbl.load('ActivityIndicator/Activity.gif')
        except Exception as e:
            print(f"Could not load activity indicator: {e}")
            # Fallback to text animation
            loading_label = tk.Label(
                container,
                text="Loading...",
                font=('Arial', 16),
                fg='#1DB954',
                bg='#000000'
            )
            loading_label.pack(pady=(100, 20))
        
        # App logo/name
        logo_frame = tk.Frame(container, bg='#000000')
        logo_frame.pack(pady=20)
        
        # Try to load logo image
        try:
            logo_pil = Image.open(r'images\app_64.png')
            logo_pil = logo_pil.resize((64, 64), Image.LANCZOS)
            
            # Convert PIL to PhotoImage
            import io
            with io.BytesIO() as output:
                logo_pil.save(output, format="PNG")
                png_data = output.getvalue()
            
            self.logo_photo = tk.PhotoImage(data=png_data)
            
            logo_img = tk.Label(
                logo_frame,
                image=self.logo_photo,
                bg='#000000'
            )
            logo_img.pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"Could not load app logo: {e}")
            # Create a simple circular logo
            logo_canvas = tk.Canvas(
                logo_frame,
                width=64,
                height=64,
                bg='#000000',
                highlightthickness=0
            )
            logo_canvas.pack(side="left", padx=(0, 15))
            
            # Draw Spotify-like circular icon
            logo_canvas.create_oval(
                4, 4, 60, 60,
                fill='#1DB954',
                outline=''
            )
            # Draw stylized "A" for Amplify
            logo_canvas.create_text(
                32, 32,
                text='A',
                font=('Arial', 32, 'bold'),
                fill='white'
            )
        
        # App title
        title = tk.Label(
            logo_frame,
            text='Amplify',
            font=('Arial', 48, 'bold'),
            fg='#FFFFFF',
            bg='#000000'
        )
        title.pack(side="left")
        
        # Tagline
        tagline = tk.Label(
            container,
            text='Your Music, Your Way',
            font=('Arial', 14),
            fg='#B3B3B3',
            bg='#000000'
        )
        tagline.pack(pady=(10, 0))
        
        # Version info
        version = tk.Label(
            container,
            text='v1.0.0',
            font=('Arial', 10),
            fg='#666666',
            bg='#000000'
        )
        version.pack(side="bottom", pady=20)
        
        # Center the splash screen
        self.update_idletasks()
        width = 600
        height = 400
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')


class Container(tk.Frame):
    """
    Main container with Spotify-like layout:
    - Row 0: Main area (Sidebar + Content) - 85%
    - Row 1: Player bar - 15%
    
    Note: Using tk.Frame instead of ctk.CTkFrame for better compatibility
    """
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, bg="#000000", *args, **kwargs)

        # ROW 0: MAIN AREA (Will be split into Sidebar + Content)
        self.main_area = tk.Frame(self, bg="#000000")
        self.main_area.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # ROW 1: PLAYER BAR
        self.player_bar = Bottom(self)
        self.player_bar.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # Configure row weights for Container
        self.grid_rowconfigure(0, weight=85)  # 85% for main area
        self.grid_rowconfigure(1, weight=15)  # 15% for player
        self.grid_columnconfigure(0, weight=1)

        # --- SPLIT MAIN_AREA INTO COLUMNS ---
        
        # COLUMN 0: SIDEBAR (Navigation)
        self.sidebar = Sidebar(self.main_area)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=8)
        
        # COLUMN 1: CONTENT (Pages)
        self.content = top.Top(self.main_area)
        self.content.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=8)
        
        # Configure column weights for main_area
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1, minsize=250)  # Sidebar min width
        self.main_area.grid_columnconfigure(1, weight=5)  # Content takes more space


class Root(ctk.CTk):
    def __init__(self, data, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.counter = False

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        
        # Hide initially
        self.withdraw()
        
        # Window setup
        self.title('Amplify')
        
        # Set icon
        try:
            # For Windows, use .ico file if available
            self.iconbitmap(r'images\app_icon.ico')
        except:
            try:
                # Fallback to PNG
                icon_photo = tk.PhotoImage(file=r"images\app_64.png")
                self.iconphoto(False, icon_photo)
            except Exception as e:
                print(f"Could not load app icon: {e}")
        
        # Set minimum size (responsive design)
        self.minsize(1200, 800)
        
        # Start maximized
        self.state('zoomed')
        
        # Show splash screen
        splash = Splash(self)
        
        def show_main_app():
            try:
                container = Container(self)
                container.grid(row=0, column=0, sticky="nsew")
                self.grid_columnconfigure(0, weight=1)
                self.grid_rowconfigure(0, weight=1)
                splash.destroy()
                self.deiconify()
            except Exception as e:
                print(f"Error creating main app: {e}")
                import traceback
                traceback.print_exc()
                splash.destroy()
                self.destroy()
        
        # Show main app after 3 seconds
        self.after(3000, show_main_app)

    def toggle_fullscreen(self, event=None):
        self.counter = not self.counter
        self.attributes("-fullscreen", self.counter)
        return "break"

    def end_fullscreen(self, event=None):
        self.counter = False
        self.attributes("-fullscreen", False)
        return "break"


if __name__ == '__main__':
    root = Root(data=None)
    root.mainloop()