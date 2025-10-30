import tkinter as tk
import tkinter.font as tkfont


class Header(tk.Frame):
    def __init__(self, master, text, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = '#000000'
        self['padx'] = 25

        # Simplified, no pyglet
        play = tkfont.Font(family="Arial", size=25, weight="bold")

        self.label = tk.Label(self,
                              text=text,
                              font=play,
                              background='#000000',
                              foreground='white')
        self.label.grid(row=0, column=0)

        # self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)