#-----Trang Đăng ký
import traceback
import tkinter as tk
from tkinter import ttk
from tkinter import font
import re
from tkinter import messagebox  


# dữ liệu đăng ký và truyền chúng
global data
data = {
	"username": "",
	"password": "",
	"phone": "",
	"email": ""
}

# data3 để truyền email
global data3
data3 = {
	"email": ""
}


# Lớp cho trường nhập: số liên lạc
class NumberEntry(tk.Entry):
	def __init__(self, master, placeholder, id, *args, **kwargs):
		tk.Entry.__init__(self, master, *args, **kwargs)

		# self.placeholder = placeholder
		self['textvariable'] = placeholder
		self.appHighlightFont = font.Font(
			family='lineto circular',
			size=12,
		)

		self.default_fg = '#867f7a'
		self.input_fg = 'white'

		self['background'] = '#404040'
		self['foreground'] = self.default_fg
		self['insertbackground'] = 'white'
		self['font'] = self.appHighlightFont
		self['border'] = 0

		def default_placeholder(self):
			# print("placeholder:", self.get())
			# self.delete(0,100)
			self.insert(0, placeholder)

		def only_numbers(char):
			return char.isdigit()

		def foc_in(event):
			# self['foreground'] = 'white'
			if self['foreground'] == self.default_fg:
				if self.get() == placeholder:
					self['foreground'] = self.default_fg
					self.delete(0, 100)
			validation = master.register(only_numbers)
			self['validate'] = 'key'
			self['validatecommand'] = (validation, '%S')
			self['foreground'] = 'white'
			self['textvariable'] = textvariable

		def foc_out(event):
		
			lambda e: enter_details(e)
			self['foreground'] = self.default_fg
			if (id == 'phone'):
				data["phone"] = self.get()
		

			if not self.get():
				default_placeholder(self)
			else:
				self.insert(0, self['textvariable'])

		def enter_details(event):
			if (id == 'phone'):
				data["phone"] = self.get()
		
		self.bind("<FocusIn>", lambda e: foc_in(e))
		self.bind("<FocusOut>", lambda e: foc_out(e))
		self.bind("<Return>", lambda e: enter_details(e))

		default_placeholder(self)


# Lớp cho các trường nhập: tên người dùng, mật khẩu, email
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
			self['foreground'] = 'white'
			self['textvariable'] = textvariable

		#hàm được gọi khi không focus
		def foc_out(event):
			self['foreground'] = self.default_fg
			
			if not self.get():
				if (show == 1):
					self['show'] = ''
				default_placeholder(self)
			else:
				self.insert(0, self['textvariable'])

		#def key(events)	
		self.bind("<FocusIn>", lambda e: foc_in(e))
		self.bind("<FocusOut>", lambda e: foc_out(e))

# Frame of Signup/Register Page
class Frame2(tk.Frame):
	def __init__(self, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)

		#Khung
		self.container = tk.Frame(self, bg='#121212', padx=80, pady=30)

		#Tiêu đề Đăng ký
		# self.logo = tk.PhotoImage(file=r'hình ảnh/signup_head.png', height=225, width=360)
		# self.labelLogo = tk.Label(self.container, image=self.logo, bd=0)
		# self.labelLogo.grid(row=0, column=0)

		#Cho nút Quay lại
		from .Frame1 import Frame1

		#Kiểu font, kích thước
		self.appHighlightFont = font.Font(
			family='lineto circular',
			size=14,
		)

		#Nút Quay lại
		self.back = tk.Button(
			self.container,
			border=0,
			text='Quay lại',
			background='#121212',
			activebackground='#121212',
			activeforeground='white',
			font=self.appHighlightFont,
			foreground='white',
			command=lambda: self.master.show_frame(Frame1)
		)
		self.back.grid(
			row=7,
			column=0,
			sticky='news',
			padx=2,
			pady=5,
			ipadx=20,
			ipady=10
		)

		#Nhập Tên người dùng
		self.username_input = tk.StringVar()
		self.username = UserEntry(
			self.container,
			placeholder="  Tên người dùng",
			show=0,
			textvariable=None,
			id="username"
		)
		self.username.grid(
			row=1,
			column=0,
			sticky=tk.N + tk.S + tk.E + tk.W,
			padx=2,
			pady=5,
			ipadx=20,
			ipady=10
		)

		#Nhập Mật khẩu
		self.password = UserEntry(
			self.container,
			placeholder="  Mật khẩu",
			show=1,
			textvariable=None,
			id="password"
		)
		self.password.grid(
			row=2,
			column=0,
			sticky=tk.N + tk.S + tk.E + tk.W,
			padx=2,
			pady=5,
			ipadx=20,
			ipady=10
		)

		#Nhập Số liên lạc
		self.phone = UserEntry(
			self.container,
			placeholder="  Số liên lạc",
			show=0,
			textvariable=None,
			id="phone",
		)
		self.phone.grid(
			row=3,
			column=0,
			sticky=tk.N + tk.S + tk.E + tk.W,
			padx=2,
			pady=5,
			ipadx=20,
			ipady=10
		)

		#Nhập Email
		self.email = UserEntry(
			self.container,
			placeholder="  Email",
			show=0,
			textvariable=None,
			id="email"
		)
		self.email.grid(
			row=4,
			column=0,
			sticky=tk.N + tk.S + tk.E + tk.W,
			padx=2,
			pady=4,
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
		self.result.grid(row=5, column=0)

		#Nút Đăng ký
		# self.btnimg = tk.PhotoImage(file=r'hình ảnh/register.png')
		
		self.register = tk.Button(
			self.container,
			border=0,
			background='#121212',
			activebackground='#121212',
			# image=self.btnimg,
			text='Đăng ký',
			command=self.registerNow
		)
		self.register.grid(row=6, column=0, pady=10)

		#Lưới khung và cấu hình
		self.container.grid(row=0, column=0)

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		# Auto-focus vào trường đầu tiên (username)
		self.username.focus_set()

		# Bind Enter key để đăng ký
		self.bind('<Return>', lambda e: self.registerNow())
		self.username.bind('<Return>', lambda e: self.registerNow())
		self.password.bind('<Return>', lambda e: self.registerNow())
		self.phone.bind('<Return>', lambda e: self.registerNow())
		self.email.bind('<Return>', lambda e: self.registerNow())

	#Hàm xác thực cho số liên lạc
	def phoneCheck(self,s):
		Pattern = re.compile(r'^(\+84|0)[3-9]\d{8}$')
		return Pattern.match(s)

	#Hàm xác thực cho email
	def emailCheck(self,s):
		Pattern = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
		return Pattern.match(s)

	#Hàm xác thực cho mật khẩu
	def passwordCheck(self,s):
		if (len(s) in range(8, 20)):
			return True
		else:
			return False

	#Xác thực cho đăng ký
	def registerNow(self):
		
		global data
		username = self.username.get()
		password = self.password.get()
		phone = self.phone.get()
		email = self.email.get()

		data["username"] = username
		data["password"] = password
		data["phone"] = phone
		data["email"] = email
	

		#các placeholder
		username_placeholder = "  Username"
		password_placeholder = "  Password"
		phone_placeholder = "  Contact Number"
		email_placeholder = "  Email ID"
	
		if username==username_placeholder or password==password_placeholder or phone==phone_placeholder or email==email_placeholder:
			self.result['text'] = "Vui lòng nhập tất cả các trường"
			return

		if username.strip(' ')=='' or password.strip(' ')=='' or phone.strip(' ')=='' or email.strip(' ')=='' :
			self.result['text'] = "Thông tin đăng nhập không hợp lệ" 
			return

		if not self.passwordCheck(password):
			self.result['text'] = "Mật khẩu phải có ít nhất 8 ký tự"
			return

		if not self.phoneCheck(phone):
			self.result['text'] = "Số điện thoại không hợp lệ"
			return

		if not self.emailCheck(email):
			self.result['text'] = "Email không hợp lệ"
			return
		data3['email'] = email
		
		# Đăng ký người dùng trực tiếp không cần xác thực email
		from Database.Database import register_user
		
		success = register_user(username, email, phone, password)
		if success:
			self.result['text'] = "Tài khoản đã được tạo thành công! Vui lòng đăng nhập."
			# Lưu user_id vào file để tự động đăng nhập
			# Hiển thị khung đăng nhập
			from .Frame3 import Frame3
			return self.master.show_frame(Frame3)
		else:
			self.result['text'] = "Email đã tồn tại hoặc đăng ký không thành công. Vui lòng thử lại."































