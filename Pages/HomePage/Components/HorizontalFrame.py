import tkinter as tk
import tkinter.font as tkfont
from Pages.Resource.HorizontalScrollableFrame import HorizontalScrollableFrame
from PIL import ImageTk, Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import requests
from io import BytesIO
import pyglet
import threading
import time
from pathlib import Path
import hashlib


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
            print(f"⏱️ Timeout (attempt {attempt + 1}/{max_retries}): {url[:50]}...")
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
            continue
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error (attempt {attempt + 1}/{max_retries}): {str(e)[:50]}...")
            if attempt < max_retries - 1:
                time.sleep(1)
            continue
            
        except Exception as e:
            print(f"❌ Error loading image: {str(e)[:50]}...")
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


class HorizontalFrame(tk.Frame):
    def __init__(self, master, controller, data, text, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = '#181818'
        self['padx'] = 20
        self['pady'] = 20

        self.controller = controller  # Store controller
        self.upper = Upper(self, text, data)
        self.line = tk.Frame(self, background='#333333', height=2)
        self.lower = Lower(self, controller, data)  # Pass controller

        self.upper.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.line.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.lower.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def right(self):
        self.lower.scrollable.right()

    def left(self):
        self.lower.scrollable.left()


class Upper(tk.Frame):
    def __init__(self, master, text, data, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = '#181818'
        self.master = master

        try:
            pyglet.font.add_file('fonts/Play/Play-Bold.ttf')
            play = tkfont.Font(family="Play", size=15, weight="bold")
        except:
            play = tkfont.Font(family="Arial", size=15, weight="bold")

        self.left = tk.PhotoImage(file=r'.\images\left_arrow.png')
        self.right = tk.PhotoImage(file=r'.\images\right_arrow.png')

        self.label = tk.Label(self,
                              text=text,
                              font=play,
                              anchor=tk.W,
                              background='#181818',
                              foreground='white')

        if len(data) > 5:
            self.left_button = ArrowButton(self, image=self.left, command=master.left)
            self.right_button = ArrowButton(self, image=self.right, command=master.right)

            self.left_button.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
            self.right_button.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

        self.label.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=100)
        self.grid_columnconfigure((1, 2), weight=1)


class Lower(tk.Frame):
    count = 0

    def __init__(self, master, controller, data, *args, **kwargs):
        from Base.listOfPage import musicPages
        musicPages.append([])
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = '#181818'
        self['pady'] = 10
        self.bind('<Configure>', self.size)

        # Store controller for navigation
        self.controller = controller
        self.data = data

        self.scrollable = HorizontalScrollableFrame(self)
        self.frame = tk.Frame(self.scrollable.scrollable_frame, bg='#181818')

        self.images = []
        self.loading_jobs = []

        # Load images asynchronously
        print(f"Loading {len(data)} images...")
        
        # Create placeholders first for instant UI
        for i, item in enumerate(data):
            placeholder = create_placeholder_image(text="Loading...")
            self.images.append(placeholder)
        
        # Create buttons with placeholders
        for i, j in enumerate(data):
            musicPages[Lower.count].append(0)
            
            # Get track info
            tracks = j.get('tracks', [])
            title = j.get('text', 'Unknown')
            artist = tracks[0].get('artist', 'Unknown Artist') if tracks else 'Unknown Artist'
            
            button = MusicCard(
                self.frame,
                self.images[i],
                title=title,
                artist=artist,
                command=lambda item_data=j: self.click(item_data)
            )
            button.grid(row=0, column=i, sticky=tk.N + tk.S + tk.E + tk.W, padx=5)
        
        # Load images in background
        for i, item in enumerate(data):
            image_url = item.get('url', '')
            if image_url and image_url.startswith('http'):
                # Load async
                threading.Thread(
                    target=self.load_image_async,
                    args=(i, image_url),
                    daemon=True
                ).start()

        self.frame.grid(row=0, column=0, sticky='nsew')
        self.scrollable.grid(row=0, column=0, sticky=tk.W + tk.E)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        Lower.count += 1

    def load_image_async(self, index, url):
        """Load image in background thread"""
        try:
            img = load_image_from_url(url, size=(300, 300))
            # Update UI in main thread
            self.after(0, lambda: self.update_image(index, img))
        except Exception as e:
            print(f"❌ Failed to load image {index}: {e}")

    def update_image(self, index, img):
        """Update image in main thread"""
        try:
            self.images[index] = img
            # Find the button and update its image
            button = self.frame.grid_slaves(row=0, column=index)[0]
            if isinstance(button, MusicCard):
                button.update_loaded_image(img)
        except Exception as e:
            print(f"❌ Error updating image {index}: {e}")

    def click(self, item_data):
        """Handle card click by showing the correct page"""
        title = item_data.get('text', 'Unknown')
        print(f"🎵 Clicked: {title}")
        
        # Check if it's an album
        if 'album_id' in item_data:
            album_id = item_data.get('album_id')
            print(f"📀 Navigating to Album ID: {album_id}")
            # TODO: Implement navigation when Top class has show_page method
            # self.controller.show_page("Album", album_id)
        
        # Check if it's an artist
        elif 'artist_id' in item_data:
            artist_id = item_data.get('artist_id')
            print(f"🎤 Navigating to Artist ID: {artist_id}")
            # TODO: Implement navigation
            # self.controller.show_page("Artist", artist_id)
        
        # It's a track
        else:
            track_id = item_data.get('track_id')
            print(f"▶️ Playing Track ID: {track_id}")
            # TODO: Add to player queue

    def size(self, event):
        global width, w, height, number
        width = event.width
        w = event.width / 5 - 14
        height = self.winfo_height()
        number = Lower.count


class ArrowButton(tk.Button):
    def __init__(self, master, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)
        self['relief'] = tk.FLAT
        self['background'] = '#181818'
        self['foreground'] = 'white'
        self['activebackground'] = '#181818'
        self['activeforeground'] = 'white'
        self['borderwidth'] = 0


class MusicCard(tk.Frame):
    """Enhanced music card with hover effects and scrolling text"""
    
    def __init__(self, master, image, title, artist, command=None, *args, **kwargs):
        tk.Frame.__init__(self, master, bg='#181818', *args, **kwargs)
        
        self.image_original = image
        self.title = title
        self.artist = artist
        self.command = command
        self.scroll_offset = 0
        self.scroll_job = None
        self.is_hovering = False
        
        # Load fonts
        try:
            pyglet.font.add_file('fonts/Play/Play-Bold.ttf')
            self.title_font = tkfont.Font(family="Play", size=13, weight="bold")
            self.artist_font = tkfont.Font(family="Play", size=11)
        except:
            self.title_font = tkfont.Font(family="Arial", size=13, weight="bold")
            self.artist_font = tkfont.Font(family="Arial", size=11)
        
        # Image button (clickable)
        self.image_button = tk.Label(self, bg='#181818', cursor='hand2')
        self.image_button.pack(pady=(0, 5))
        
        # Title label with scrolling support
        self.title_canvas = tk.Canvas(self, bg='#181818', highlightthickness=0, height=20)
        self.title_canvas.pack(fill=tk.X, padx=5)
        
        # Artist label
        self.artist_label = tk.Label(
            self,
            text=self.truncate_text(artist, 25),
            font=self.artist_font,
            bg='#181818',
            fg='#B3B3B3',
            anchor=tk.W,
            justify=tk.LEFT
        )
        self.artist_label.pack(fill=tk.X, padx=5)
        
        # Bind events
        self.bind('<Configure>', self.on_resize)
        self.image_button.bind('<Button-1>', self.on_click)
        self.image_button.bind('<Enter>', self.on_enter)
        self.image_button.bind('<Leave>', self.on_leave)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
        # Draw initial title
        self.draw_title()
        
        # Set initial image
        self.on_resize(None)
    
    def update_loaded_image(self, new_image):
        """Update image after async loading"""
        self.image_original = new_image
        global width
        w = width / 5 - 14 if 'width' in globals() else 200
        img_size = int(round(w))
        self.update_image(img_size, shadow=self.is_hovering, play_overlay=self.is_hovering)
    
    def truncate_text(self, text, max_length):
        """Truncate text with ellipsis"""
        if len(text) > max_length:
            return text[:max_length-3] + '...'
        return text
    
    def draw_title(self):
        """Draw title text on canvas"""
        self.title_canvas.delete('all')
        
        # Calculate text width
        title_text = self.title if len(self.title) <= 30 else self.title
        
        # Draw text
        self.title_canvas.create_text(
            -self.scroll_offset,
            10,
            text=title_text,
            font=self.title_font,
            fill='white',
            anchor=tk.W,
            tags='title'
        )
    
    def start_scrolling(self):
        """Start scrolling animation for long titles"""
        if len(self.title) <= 25:
            return
        
        self.is_hovering = True
        self.scroll_text()
    
    def scroll_text(self):
        """Scroll text animation"""
        if not self.is_hovering:
            return
        
        # Get text width
        title_width = self.title_font.measure(self.title)
        canvas_width = self.title_canvas.winfo_width()
        
        # Scroll
        self.scroll_offset += 2
        
        # Reset when fully scrolled
        if self.scroll_offset > title_width:
            self.scroll_offset = -50  # Add gap before repeating
        
        self.draw_title()
        
        # Schedule next frame
        self.scroll_job = self.after(50, self.scroll_text)
    
    def stop_scrolling(self):
        """Stop scrolling animation"""
        self.is_hovering = False
        if self.scroll_job:
            self.after_cancel(self.scroll_job)
            self.scroll_job = None
        
        # Reset scroll position
        self.scroll_offset = 0
        self.draw_title()
    
    def on_resize(self, event):
        """Handle resize event"""
        global width
        w = width / 5 - 14 if 'width' in globals() else 200
        
        # Resize image
        img_size = int(round(w))
        self.update_image(img_size, shadow=False)
    
    def update_image(self, size, shadow=False, play_overlay=False):
        """Update image with effects - MAINTAINS ASPECT RATIO"""
        # Resize and crop to maintain aspect ratio
        img = resize_and_crop(self.image_original, (size, size))
        
        # Add shadow effect on hover
        if shadow:
            # Create shadow
            shadow_img = Image.new('RGBA', (size + 10, size + 10), (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_img)
            shadow_draw.rectangle([(5, 5), (size + 5, size + 5)], fill=(0, 0, 0, 100))
            shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(5))
            
            # Paste original image on shadow
            shadow_img.paste(img, (0, 0))
            img = shadow_img.convert('RGB')
        
        # Add play button overlay on hover
        if play_overlay:
            overlay = img.copy()
            draw = ImageDraw.Draw(overlay, 'RGBA')
            
            # Semi-transparent black overlay
            draw.rectangle([(0, 0), (size, size)], fill=(0, 0, 0, 100))
            
            # Play button circle
            center = size // 2
            radius = size // 6
            draw.ellipse(
                [(center - radius, center - radius), (center + radius, center + radius)],
                fill=(30, 215, 96, 255),
                outline=(30, 215, 96, 255)
            )
            
            # Play triangle
            triangle = [
                (center - radius // 3, center - radius // 2),
                (center - radius // 3, center + radius // 2),
                (center + radius // 2, center)
            ]
            draw.polygon(triangle, fill='white')
            
            img = overlay
        
        # Update label
        self.photo = ImageTk.PhotoImage(img)
        self.image_button.config(image=self.photo)
    
    def on_enter(self, event):
        """Handle mouse enter"""
        global width
        w = width / 5 - 14 if 'width' in globals() else 200
        
        # Enlarge image with effects
        img_size = int(round(w)) + 8
        self.update_image(img_size, shadow=True, play_overlay=True)
        
        # Change artist color
        self.artist_label.config(fg='white')
        
        # Start scrolling title
        self.start_scrolling()
    
    def on_leave(self, event):
        """Handle mouse leave"""
        global width
        w = width / 5 - 14 if 'width' in globals() else 200
        
        # Reset image
        img_size = int(round(w))
        self.update_image(img_size, shadow=False, play_overlay=False)
        
        # Reset artist color
        self.artist_label.config(fg='#B3B3B3')
        
        # Stop scrolling
        self.stop_scrolling()
    
    def on_click(self, event):
        """Handle click"""
        if self.command:
            self.command()


# Keep old CardButton for compatibility
class CardButton(tk.Button):
    def __init__(self, master, url, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)
        self.url = url

        self.bind('<Configure>', self.size)

        try:
            pyglet.font.add_file('fonts/Play/Play-Bold.ttf')
            play = tkfont.Font(family="Play", size=12, weight="bold")
        except:
            play = tkfont.Font(family="Arial", size=12, weight="bold")

        self['background'] = '#181818'
        self['height'] = 300
        self['border'] = 0
        self['font'] = play
        self['compound'] = tk.TOP
        self['activebackground'] = '#181818'
        self['foreground'] = 'white'
        self['activeforeground'] = 'white'

        self.bind('<Enter>', self.enter)
        self.bind('<Leave>', self.leave)

    def size(self, event):
        global width
        w = width / 5 - 14
        self.configure(width=int(round(w)), height=int(round(w)) + 50)
        self.image = self.url
        self.image = self.image.resize((int(round(w)), int(round(w))), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.config(image=self.image)

    def enter(self, event):
        global width
        w = width / 5 - 14
        self.configure(width=int(round(w)), height=int(round(w)) + 50)
        self.image = self.url
        self.image = self.image.resize((int(round(w))+5, int(round(w))+5), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.config(image=self.image)

    def leave(self, event):
        global width
        w = width / 5 - 14
        self.configure(width=int(round(w)), height=int(round(w)) + 50)
        self.image = self.url
        self.image = self.image.resize((int(round(w)), int(round(w))), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.config(image=self.image)

