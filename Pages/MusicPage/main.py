import tkinter as tk
from PIL import Image, ImageTk


class Main(tk.Frame):
    flag = 0

    def __init__(self, master, *args, **kwargs):
        self.data = kwargs.pop('data', [])
        self.image = kwargs.pop('image', None)
        self.text = kwargs.pop('text', 'Music')
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = '#181818'

        self.bind('<Configure>', self.size)

        # Simplified version - just show title for now
        label = tk.Label(self, 
                        text=f'Music Page: {self.text}', 
                        font=('Arial', 24, 'bold'),
                        bg='#181818',
                        fg='white')
        label.pack(pady=50)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_propagate(False)

    def size(self, event):
        if Main.flag == 0:
            self.config(width=event.width)
            Main.flag = 1
    
    def update(self):
        # Override update to prevent errors
        pass