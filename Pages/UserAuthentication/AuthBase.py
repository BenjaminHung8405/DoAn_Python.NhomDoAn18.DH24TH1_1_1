#-----Cơ sở cho Xác thực-----

import tkinter as tk
from .Frame1 import Frame1
from .Frame2 import Frame2
from .Frame3 import Frame3
from .Frame4 import Frame4
from main import Root

#Bố cục của Cơ sở
class AuthBase(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Login')
        # Sử dụng attributes cho fullscreen/maximize đa nền tảng
        try:
            self.state('zoomed')  # Windows
        except tk.TclError:
            # Linux/macOS: phóng to bằng geometry hoặc -fullscreen
            self.attributes('-zoomed', True)  # Một số môi trường desktop Linux
        except:
            pass  # Dự phòng: cửa sổ bình thường

        self.frame = AuthFrame(self)
        self.frame.grid(row=0, column=0, sticky='nsew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
      

#Khung của Cơ sở
class AuthFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        #Canvas cho Hình nền
        canvas = tk.Canvas(self, width=1920, height=1280, bd=0)
        self.bg = tk.PhotoImage(file=r"images/bg4.png")
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg)
        canvas.grid(row=0, column=0)

        #Các Khung
        self.frames = {}

        for F in (Frame1, Frame2, Frame3, Frame4):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0)

        #Nút Đóng
        self.close = tk.PhotoImage(file=r"images/close3.png")
        self.button = tk.Button(
            self,
            bd=0,
            image=self.close,
            background='#121212',
            foreground='white',
            command=self.master.destroy)
        self.button.grid(row=0, column=0, pady=3, padx=3, sticky='ne')

        #Lưới khung và cấu hình
        self.show_frame(Frame1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    #Hàm hiển thị các khung
    def show_frame(self, context):
        frame  = context(self)
        frame.grid(row=0, column=0)
        # framee = self.các khung[context]
        frame.tkraise()

    #Hàm vào Trang chủ
    def login(self,user_object):
      
        """
            Check different condition for authentication
        """
        if False:
            return

      

        self.master.destroy()
        main = Root(data=user_object)
        main.mainloop()

    def openFrame4(self):
        framee = self.frames[Frame4]
        framee.tkraise()
    def openFrame3(self):
        framee = self.frames[Frame3]
        framee.tkraise()


