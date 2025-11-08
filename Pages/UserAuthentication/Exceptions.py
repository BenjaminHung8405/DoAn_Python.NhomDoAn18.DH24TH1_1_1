import tkinter as tk
from tkinter import messagebox
def Email_already_exists():
    messagebox.showerror('Lỗi','Người dùng với email đã cung cấp \nđã tồn tại.')
def Phone_already_exists():
    messagebox.showerror('Lỗi','Người dùng với số điện thoại đã cung cấp \nđã tồn tại.')
def User_not_Found():
    messagebox.showerror('Lỗi','Không tìm thấy bản ghi người dùng \ncho mã định danh đã cho.')
def Invalid_credentials():
    messagebox.showerror('Thông tin đăng nhập không hợp lệ','Vui lòng kiểm tra email \nhoặc mật khẩu của bạn.')




