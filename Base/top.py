import customtkinter as ctk
from Pages.HomePage.Home import Home
from Pages.SearchPage.SearchPage import SearchPage
from Pages.Browse.browse import Browse
from Pages.AlbumPage.Album import Album
from Pages.ArtistPage.Artist import Artist
from Pages.UserPage.UserPage import UserPage


class Top(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, fg_color="transparent", *args, **kwargs)
        
        # Store pages
        self.pages = {}
        
        # Create all pages
        for F in (Home, SearchPage, Browse, Album, Artist, UserPage):
            page_name = F.__name__
            frame = F(self, self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Show Home by default
        self.show_page("Home")

    def show_page(self, page_name, data=None):
        """Show a page and optionally pass data to it"""
        page = self.pages.get(page_name)
        if not page:
            print(f"Page not found: {page_name}")
            return
        
        # Check if page has update_data method
        if hasattr(page, 'update_data') and callable(page.update_data) and data is not None:
            page.update_data(data)
        
        # Raise the page to front
        page.tkraise()