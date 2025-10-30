import tkinter as tk


class Artist(tk.Frame):
    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = '#181818'
        
        label = tk.Label(self, 
                        text='Artists Page', 
                        font=('Arial', 24, 'bold'),
                        bg='#181818',
                        fg='white')
        label.pack(pady=50)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)