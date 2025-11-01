import customtkinter as ctk
from Pages.Resource.VerticalScrollableFrame import ScrollableFrame


class Album(ctk.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, fg_color='#121212', corner_radius=8, *args, **kwargs)
        
        self.controller = controller
        
        # Initial placeholder
        self.label = ctk.CTkLabel(
            self, 
            text='Album Page\n(Click an album to view details)', 
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="white"
        )
        self.label.pack(pady=50)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
    def update_data(self, album_id):
        """Called by controller to update page content"""
        if not album_id:
            return
            
        # Clear old content
        for widget in self.winfo_children():
            widget.destroy()
            
        # TODO: Fetch album details from database
        # from Database.Albumdata import get_album_details
        # album_details = get_album_details(album_id)
        
        # Mock data for now
        album_details = {
            'title': f'Album #{album_id}',
            'artist': 'Various Artists',
            'year': '2024',
            'tracks': [
                {'title': 'Track 1', 'duration': '3:45'},
                {'title': 'Track 2', 'duration': '4:12'},
                {'title': 'Track 3', 'duration': '2:58'},
            ]
        }
        
        # Create scrollable content
        scrollable = ScrollableFrame(self)
        scrollable.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Album header
        header_frame = ctk.CTkFrame(scrollable.scrollable_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text=album_details['title'],
            font=ctk.CTkFont(family="Arial", size=48, weight="bold"),
            text_color="white",
            anchor="w"
        )
        title.pack(fill="x")
        
        artist = ctk.CTkLabel(
            header_frame,
            text=album_details['artist'],
            font=ctk.CTkFont(size=16),
            text_color="#B3B3B3",
            anchor="w"
        )
        artist.pack(fill="x", pady=(5, 0))
        
        # Play button
        play_btn = ctk.CTkButton(
            scrollable.scrollable_frame,
            text="▶ Play",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1DB954",
            hover_color="#1ED760",
            height=50,
            width=120,
            corner_radius=25
        )
        play_btn.pack(pady=20, anchor="w")
        
        # Track list
        tracks_label = ctk.CTkLabel(
            scrollable.scrollable_frame,
            text="Tracks",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white",
            anchor="w"
        )
        tracks_label.pack(fill="x", pady=(20, 10))
        
        for i, track in enumerate(album_details['tracks'], 1):
            track_frame = ctk.CTkFrame(scrollable.scrollable_frame, fg_color="#282828", corner_radius=4)
            track_frame.pack(fill="x", pady=2)
            
            track_btn = ctk.CTkButton(
                track_frame,
                text=f"{i}. {track['title']} • {track['duration']}",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                hover_color="#404040",
                text_color="white",
                anchor="w",
                height=50
            )
            track_btn.pack(fill="x", padx=10)