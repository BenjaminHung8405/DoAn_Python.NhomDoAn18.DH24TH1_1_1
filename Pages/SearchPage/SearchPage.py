import tkinter as tk


class SearchPage(tk.Frame):
    def __init__(self, master, controller, data, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = '#181818'
        
        label = tk.Label(self, 
                        text=f'Search Results: {data}', 
                        font=('Arial', 24, 'bold'),
                        bg='#181818',
                        fg='white')
        label.pack(pady=50)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)