import tkinter as tk
import sys
import os

# Import theme mới
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS


class Bottom(tk.Frame):
	"""Bottom bar - Music player control với theme hiện đại"""
	def __init__(self, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)
		# Sử dụng màu card đẹp hơn thay vì #2c2c2c
		self['bg'] = COLORS['bg_card']
		self['highlightbackground'] = COLORS['border']
		self['highlightthickness'] = 1

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.grid_propagate(False)

	def show_frame(self, title):
		from Base.listOfPage import bottomPage
		frame = bottomPage[0]
		frame.grid(row=0, column=0, sticky='nsew')
		frame.tkraise()
