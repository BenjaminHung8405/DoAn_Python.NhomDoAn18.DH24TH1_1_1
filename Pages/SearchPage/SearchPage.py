import customtkinter as ctk
from Pages.Resource.VerticalScrollableFrame import ScrollableFrame


class SearchPage(ctk.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, fg_color='#121212', corner_radius=8, *args, **kwargs)
        
        # Header
        header = ctk.CTkLabel(
            self, 
            text='Search', 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="white",
            anchor="w"
        )
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        # Search input
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="What do you want to listen to?",
            height=40,
            font=ctk.CTkFont(size=14),
            border_width=0,
            corner_radius=20
        )
        self.search_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Results area (placeholder)
        self.results_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.results_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        placeholder = ctk.CTkLabel(
            self.results_frame,
            text="🔍 Start typing to search...",
            font=ctk.CTkFont(size=16),
            text_color="#B3B3B3"
        )
        placeholder.pack(pady=50)
        
        # Configure grid
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Search input
        self.grid_rowconfigure(2, weight=1)  # Results
        self.grid_columnconfigure(0, weight=1)