import tkinter as tk
from Pages.Resource.VerticalScrollableFrame import ScrollableFrame
from Pages.Resource.Header import Header
from Pages.HomePage.Components.HorizontalFrame import HorizontalFrame
import Database.HomePagedata as data


class Home(tk.Frame):
    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = '#181818'

        # Add header - use GRID instead of pack
        self.head = Header(self, text='Home')
        self.head.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Create scrollable frame for content - use GRID instead of pack
        self.scrollable = ScrollableFrame(self)
        
        # Get data from database
        try:
            homepage_data = data.get_data()
            print(f"✓ Loaded {len(homepage_data)} sections from database")
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            homepage_data = []
        
        # Create horizontal frames for each section
        for section in homepage_data:
            try:
                frame = HorizontalFrame(
                    self.scrollable.scrollable_frame,
                    controller,
                    section['data'],
                    section['name']
                )
                frame.pack(fill=tk.BOTH, expand=True, pady=10)
            except Exception as e:
                print(f"✗ Error creating section {section.get('name', 'Unknown')}: {e}")

        self.scrollable.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=0)  # Header - fixed height
        self.grid_rowconfigure(1, weight=1)  # Scrollable - expandable
        self.grid_columnconfigure(0, weight=1)