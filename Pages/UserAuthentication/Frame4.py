#-----Trang Xác thực Email-----

import tkinter as tk
from tkinter import ttk
from tkinter import font
import re

# data2 để kiểm tra thông tin đăng nhập và truyền chúng
global data3
data3 = {
	# "email": "",
	"otp": "",
}

#truyền thông tin đăng nhập người dùng vào Trang chủ
global state2
state2 = {
	'user_object': None
}


#Lớp cho widget Entry
class UserEntry(tk.Entry):
	def __init__(self, master, placeholder, show, textvariable, id, *args, **kwargs):
		tk.Entry.__init__(self, master, *args, **kwargs)

		#hàm placeholder
		def default_placeholder(self):
			self.insert(0, placeholder)

		default_placeholder(self)

		#kích thước font, kiểu
		self.appHighlightFont = font.Font(
			family='lineto circular',
			size=12,
		)

		#màu font
		self.default_fg = '#867f7a'
		self.input_fg = 'white'

		#thuộc tính của widget Entry
		self['background'] = '#404040'
		self['foreground'] = self.default_fg
		self['insertbackground'] = 'white'
		self['font'] = self.appHighlightFont
		self['border'] = 0

		#hàm được gọi khi focus
		def foc_in(event):
			if (show == 1):
				self['show'] = '*'
			if self['foreground'] == self.default_fg:
				if self.get() == placeholder:
					self['foreground'] = self.default_fg
					self.delete(0, 100)
			self['textvariable'] = textvariable
			self['foreground'] = 'white'
			
		#hàm được gọi khi không focus
		def foc_out(event):
			lambda e: enter_details(e)
			self['foreground'] = self.default_fg
			# print(self.get())
			if not self.get():
				if (show == 1):
					self['show'] = ''
				default_placeholder(self)
			else:
				self.insert(0, self['textvariable'])
		
		#def key(events):
		self.bind("<FocusIn>", lambda e: foc_in(e))
		self.bind("<FocusOut>", lambda e: foc_out(e))

#Khung of Email Verification Page
class Frame4(tk.Frame):
	def __init__(self, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)

		#Khung
		self.container = tk.Frame(self, bg='#121212', padx=80, pady=80)

		#Tiêu đề Xác thực Email
		self.logo = tk.PhotoImage(file=r'images/login_head2.png', height=150, width=360)
		self.labelLogo = tk.Label(self.container, image=self.logo, bd=0)
		self.labelLogo.grid(row=0, column=0, pady=25)

		#Cho nút Quay lại
		from .Frame1 import Frame1
	
		#Kiểu font, kích thước
		self.appHighlightFont = font.Font(
			family='lineto circular',
			size=14
		)

		#Nút Quay lại
		self.back = tk.Button(
			self.container,
			border=0,
			text='Back',
			background='#121212',
			activebackground='#121212',
			foreground='white',
			activeforeground='white',
			font=self.appHighlightFont,
			command=lambda: self.master.show_frame(Frame1)
		) 
		self.back.grid(
			row=5,
			column=0,
			sticky='news',
			padx=2,
			pady=5,
			ipadx=20,
			ipady=10
		)
		

		

		#Nhập mã OTP
		self.otp = UserEntry(
			self.container,
			placeholder="  OTP",
			show=0,
			textvariable=None,
			id="otp"
		)
		self.otp.grid(
			row=2,
			column=0,
			sticky=tk.N + tk.S + tk.E + tk.W,
			padx=2,
			pady=5,
			ipadx=20,
			ipady=10
		)

		#Hiển thị Kết quả/Trạng thái
		self.result = tk.Label(
			self.container,
			border=0,
			background='#121212',
			activebackground='#121212',
			foreground='white',
			activeforeground='white',
			# font=appHighlightFont,
		)
		self.result.grid(row=3, column=0)

		#Nút Xác thực
		self.btnimg = tk.PhotoImage(file=r'images/verify.png')

		self.Verify = tk.Button(
			self.container,
			border=0,
			background='#121212',
			activebackground='#121212',
			image=self.btnimg,
			# command=self.master.login
			command=self.verifyNow
		)
		self.Verify.grid(row=4, column=0, pady=10)

		#Lưới khung và cấu hình
		self.container.grid(row=0, column=0)

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		self.appHighlightFont = font.Font( 
			family='lineto circular',
			size=14
		)

		#nút gửi lại
		self.resend = tk.Button(
			self.container,
			border=0,
			text="Resend OTP",
			background='#121212',
			activebackground='#121212',
			foreground='white',
			activeforeground='white',
			font=self.appHighlightFont,
			command=self.resend_OTP
		) 
		self.resend.grid(
			row=5,
			column=0,
			sticky='news',
			padx=2,
			pady=5,
			ipadx=20,
			ipady=10
		)

	#Gửi lại OTP
	def resend_OTP(self):
		from Database.Database import send_email_verification_otp
		send_email_verification_otp(data3['email'])

	#Hàm xác thực cho OTP
	def otpCheck(self, s):
		if len(s)==6 :
			return True
		else:
			return False 
	
	#Xác thực cho đăng nhập
	def verifyNow(self):
		
		global data2
		otp = self.otp.get()
		
	
		data3['otp'] = otp 
	

		#các placeholder
		
		otp_placeholder = "  OTP"

		

		if otp.strip(' ') == '' :
			self.result['text'] = "Invalid Credentials"
			return

		

		if not self.otpCheck(otp):
			self.result['text'] = "otp must be atleast 6 characters long"
			return
		from Database.Database import verify_email_database
		if verify_email_database(data3['email'],otp) : 
			
			self.master.openFrame3()
		else:
			self.result['text'] = "Invalid OTP"
			return
 
		
		




