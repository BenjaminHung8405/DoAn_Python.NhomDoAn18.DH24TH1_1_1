import customtkinter as ctk
from Pages.Resource.VerticalScrollableFrame import ScrollableFrame


class Browse(ctk.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, fg_color='#121212', corner_radius=8, *args, **kwargs)
        
        # Header
        header = ctk.CTkLabel(
            self, 
            text='Browse All', 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="white",
            anchor="w"
        )
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        # Scrollable content
        scrollable = ScrollableFrame(self)
        scrollable.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 20))
        
        # Genre cards (placeholder)
        genres = [
            ("🎵 Pop", "#E13300"),
            ("🎸 Rock", "#DC148C"),
            ("🎹 Jazz", "#1E3264"),
            ("🎤 Hip-Hop", "#B49BC8"),
            ("🎼 Classical", "#8D67AB"),
            ("🎧 Electronic", "#1E3A8A"),
        ]
        
        # Create grid of genre cards
        row, col = 0, 0
        for genre_name, color in genres:
            card = ctk.CTkButton(
                scrollable.scrollable_frame,
                text=genre_name,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=color,
                hover_color=self.lighten_color(color),
                height=100,
                corner_radius=8,
                command=lambda g=genre_name: self.on_genre_click(g)
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
        
        # Configure grid
        scrollable.scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Scrollable
        self.grid_columnconfigure(0, weight=1)
    
    def lighten_color(self, hex_color):
        """Lighten a hex color for hover effect"""
        # Simple implementation - increase brightness
        return hex_color  # You can implement actual color lightening
    
    def on_genre_click(self, genre_name):
        """Handle genre card click"""
        print(f"Genre clicked: {genre_name}")