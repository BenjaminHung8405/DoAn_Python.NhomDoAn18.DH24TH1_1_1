import tkinter as tk
from Base import top
from Base.bottom import Bottom
from ActivityIndicator.Activity_Indicator import ImageLabel


class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Splash")
        self['bg'] = 'black'

        lbl = ImageLabel(self)
        lbl['bd'] = 0
        lbl['bg'] = 'black'
        lbl.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.logo = tk.PhotoImage(file=r'images/loading.png', height=150, width=360)
        self.labelLogo = tk.Label(self, image=self.logo, bd=0, bg='black')
        self.labelLogo.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.grid_columnconfigure(0, weight=1)
        # Sử dụng attributes cho cửa sổ phóng to trên Linux
        try:
            self.state('zoomed')
        except:
            self.attributes('-zoomed', True)
        # self.overrideredirect(True)  # Removed for better UX - allows window controls

        lbl.load('ActivityIndicator/Activity.gif')


class Container(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, bg='#000000', *args, **kwargs)

        self.top = top.Top(self)
        self.bottom = Bottom(self)

        from Base.listOfPage import bottomInstance
        bottomInstance.append(self.bottom)

        self.top.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.bottom.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.grid_rowconfigure(0, weight=8)
        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(0, weight=1)


class Root(tk.Tk):
    def __init__(self, data, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.counter = False

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        # Hide main window initially
        self.withdraw()
        
        # Show splash screen
        splash = Splash(self)
        
        # Schedule main window creation after splash
        self.after(5000, lambda: self.create_main_window(splash, data))
    
    def create_main_window(self, splash, data):
        """Create the main application window after splash screen"""
        # Destroy splash
        splash.destroy()
        
        # Setup main window
        self.title('Amplify')
        app_icon = tk.PhotoImage(file=r"images/app_64.png")
        self.iconphoto(False, app_icon)

        container = Container(self)
        container.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Phóng to cửa sổ - tương thích đa nền tảng
        try:
            self.state('zoomed')
        except:
            self.attributes('-zoomed', True)
        
        # Show main window
        self.deiconify()

 

    def toggle_fullscreen(self, event=None):
        self.counter = not self.counter  # Chỉ đảo ngược boolean
        self.attributes("-fullscreen", self.counter)
        return "break"

    def end_fullscreen(self, event=None):
        self.counter = False
        self.attributes("-fullscreen", False)
        return "break"


if __name__ == '__main__':
    from Database.Database import get_user
    

    from os import path

    if path.exists('user'):
        f = open('user', 'r')
        doc = get_user(f.readline().strip())
        f.close()

        # Nếu không tìm thấy người dùng, hiển thị màn hình đăng nhập
        if doc:
            root = Root(data=doc)
            root.mainloop()
        else:
            from Pages.UserAuthentication.AuthBase import AuthBase
            login = AuthBase()
            login.mainloop()
    else:
        from Pages.UserAuthentication.AuthBase import AuthBase

        login = AuthBase()
        login.mainloop()
