import customtkinter as ctk
from PIL import Image


class Sidebar(ctk.CTkFrame):
    """
    Spotify-like sidebar with navigation menu
    """
    def __init__(self, master, *args, **kwargs):
        ctk.CTkFrame.__init__(
            self, 
            master, 
            fg_color="#121212",
            corner_radius=8,
            *args, 
            **kwargs
        )
        
        # Configure grid
        self.grid_rowconfigure(0, weight=0)  # Logo
        self.grid_rowconfigure(1, weight=0)  # Menu items
        self.grid_rowconfigure(2, weight=1)  # Spacer
        self.grid_rowconfigure(3, weight=0)  # Playlists
        self.grid_columnconfigure(0, weight=1)
        
        # --- LOGO SECTION ---
        self.create_logo_section()
        
        # --- MAIN MENU SECTION ---
        self.create_main_menu()
        
        # --- PLAYLISTS SECTION ---
        # Spacer
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.grid(row=2, column=0, sticky="nsew")
        
        self.create_playlists_section()
    
    def create_logo_section(self):
        """Create logo/brand section"""
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(20, 30))
        
        try:
            # Load logo using CTkImage (supports HighDPI)
            logo_pil = Image.open(r"images\app_64.png")
            self.logo_img = ctk.CTkImage(
                light_image=logo_pil,
                dark_image=logo_pil,
                size=(32, 32)  # Display size
            )
            logo_label = ctk.CTkLabel(
                logo_frame,
                image=self.logo_img,
                text="",
                fg_color="transparent"
            )
            logo_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print(f"Could not load logo: {e}")
        
        # App name
        title = ctk.CTkLabel(
            logo_frame,
            text="Amplify",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="white",
            fg_color="transparent"
        )
        title.pack(side="left")
    
    def create_main_menu(self):
        """Create main navigation menu"""
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 20))
        
        # Menu items with icons
        menu_items = [
            ("home", "Home"),
            ("search", "Search"),
            ("library", "Your Library"),
        ]
        
        for icon_name, text in menu_items:
            btn = MenuButton(
                menu_frame,
                icon_name=icon_name,
                text=text,
                command=lambda t=text: self.on_menu_click(t)
            )
            btn.pack(fill="x", pady=2)
    
    def create_playlists_section(self):
        """Create playlists section"""
        playlist_frame = ctk.CTkFrame(self, fg_color="transparent")
        playlist_frame.grid(row=3, column=0, sticky="nsew", padx=15, pady=(0, 20))
        
        # Section title
        title = ctk.CTkLabel(
            playlist_frame,
            text="PLAYLISTS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#B3B3B3",
            anchor="w"
        )
        title.pack(fill="x", pady=(0, 10))
        
        # Scrollable playlist list
        scrollable = ctk.CTkScrollableFrame(
            playlist_frame,
            fg_color="transparent",
            scrollbar_button_color="#282828",
            scrollbar_button_hover_color="#404040"
        )
        scrollable.pack(fill="both", expand=True)
        
        # Sample playlists
        playlists = ["❤️ Liked Songs", "🎵 My Playlist #1", "😎 Chill Vibes", "💪 Workout Mix"]
        for playlist in playlists:
            btn = ctk.CTkButton(
                scrollable,
                text=playlist,
                font=ctk.CTkFont(size=12),
                fg_color="transparent",
                hover_color="#282828",
                text_color="#B3B3B3",
                anchor="w",
                height=32,
                command=lambda p=playlist: self.on_playlist_click(p)
            )
            btn.pack(fill="x", pady=1)
    
    def on_menu_click(self, menu_name):
        """Handle menu item click"""
        print(f"Menu clicked: {menu_name}")
        # TODO: Navigate to page
    
    def on_playlist_click(self, playlist_name):
        """Handle playlist click"""
        print(f"Playlist clicked: {playlist_name}")
        # TODO: Navigate to playlist


class MenuButton(ctk.CTkButton):
    """Custom menu button with icon and text"""
    def __init__(self, master, icon_name, text, *args, **kwargs):
        # Icon mapping (you can create actual icon images later)
        icons = {
            "home": "🏠",
            "search": "🔍",
            "library": "📚"
        }
        
        icon = icons.get(icon_name, "•")
        
        ctk.CTkButton.__init__(
            self,
            master,
            text=f"{icon}  {text}",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent",
            hover_color="#282828",
            text_color="white",
            anchor="w",
            height=40,
            corner_radius=4,
            *args,
            **kwargs
        )