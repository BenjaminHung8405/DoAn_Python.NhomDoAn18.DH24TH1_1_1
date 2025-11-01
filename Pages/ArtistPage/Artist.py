import customtkinter as ctk
from Pages.Resource.VerticalScrollableFrame import ScrollableFrame


class Artist(ctk.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, fg_color='#121212', corner_radius=8, *args, **kwargs)
        
        self.controller = controller
        
        # Initial placeholder
        self.label = ctk.CTkLabel(
            self, 
            text='Artist Page\n(Click an artist to view details)', 
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="white"
        )
        self.label.pack(pady=50)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)