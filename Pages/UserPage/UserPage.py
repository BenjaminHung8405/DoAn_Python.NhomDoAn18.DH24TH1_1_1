import customtkinter as ctk


class UserPage(ctk.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, fg_color='#121212', corner_radius=8, *args, **kwargs)
        
        # Header
        header = ctk.CTkLabel(
            self, 
            text='Your Profile', 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="white",
            anchor="w"
        )
        header.pack(padx=20, pady=20, fill="x")
        
        # Profile info
        info_frame = ctk.CTkFrame(self, fg_color="#282828", corner_radius=8)
        info_frame.pack(padx=20, pady=10, fill="x")
        
        name_label = ctk.CTkLabel(
            info_frame,
            text="👤 Guest User",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        name_label.pack(padx=20, pady=10, anchor="w")
        
        stats = ctk.CTkLabel(
            info_frame,
            text="0 Playlists • 0 Liked Songs",
            font=ctk.CTkFont(size=14),
            text_color="#B3B3B3"
        )
        stats.pack(padx=20, pady=(0, 10), anchor="w")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)