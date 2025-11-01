import tkinter as tk
import tkinter.font as tkfont


class Header(tk.Frame):
    """Reusable header component for pages"""
    def __init__(self, master, text='', *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = '#181818'
        self['height'] = 80
        
        try:
            import pyglet
            pyglet.font.add_file('fonts/Play/Play-Bold.ttf')
            font = tkfont.Font(family="Play", size=32, weight="bold")
        except:
            font = tkfont.Font(family="Arial", size=32, weight="bold")
        
        self.label = tk.Label(
            self,
            text=text,
            font=font,
            bg='#181818',
            fg='white',
            anchor=tk.W,
            padx=20,
            pady=20
        )
        self.label.pack(fill=tk.BOTH, expand=True)
    
    def set_text(self, text):
        """Update header text"""
        self.label.config(text=text)