import tkinter as tk
import sys
import os

# Import theme mới
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS


class TopRightBottom(tk.Frame):
	"""Container cho các trang nội dung với theme hiện đại"""
	def __init__(self, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)
		# Sử dụng màu nền secondary
		self['background'] = COLORS['bg_secondary']

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.grid_propagate(False)

