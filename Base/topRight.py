import tkinter as tk
from .topRightTop import TopRightTop
from .topRightBottom import TopRightBottom
import sys
import os

# Import theme mới
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS


class TopRight(tk.Frame):
    """Main content area - Phần bên phải với theme hiện đại"""
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        # Sử dụng màu nền primary thay vì purple
        self['background'] = COLORS['bg_primary']

        self.topRightTop = TopRightTop(self)
        self.topRightBottom = TopRightBottom(self)

        self.topRightTop.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.topRightBottom.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=40)
        self.grid_columnconfigure(0, weight=1)
