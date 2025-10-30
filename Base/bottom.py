import tkinter as tk


class Bottom(tk.Frame):
	def __init__(self, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)
		self['bg'] = '#2c2c2c'

		# Simple placeholder for music player
		label = tk.Label(self, 
		                text='Music Player Controls', 
		                bg='#2c2c2c', 
		                fg='white',
		                font=('Arial', 12))
		label.pack(pady=10)

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.grid_propagate(False)

	def show_frame(self, title):
		# Placeholder method
		pass