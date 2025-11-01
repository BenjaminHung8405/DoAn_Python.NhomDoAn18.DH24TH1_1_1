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

        self.logo = tk.PhotoImage(file=r'images\loading.png', height=150, width=360)
        self.labelLogo = tk.Label(self, image=self.logo, bd=0, bg='black')
        self.labelLogo.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.grid_columnconfigure(0, weight=1)
        self.geometry('1600x900')
        # Center the splash screen
        self.update_idletasks()
        width = 1600
        height = 900
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.overrideredirect(True)

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
        
        # Setup main window
        self.title('Amplify')
        app_icon = tk.PhotoImage(file=r"images\app_64.png")
        self.iconphoto(False, app_icon)
        self.geometry('1600x900')
        
        # Center the main window
        self.update_idletasks()
        width = 1600
        height = 900
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Comment this line to show on taskbar
        # self.overrideredirect(True)

        # Show splash screen
        splash = Splash(self)
        
        # Create container after splash is shown
        def show_main_app():
            container = Container(self)
            container.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            splash.destroy()
            self.deiconify()
        
        # Show main app after 3 seconds (instead of 30!)
        self.after(3000, show_main_app)

    def toggle_fullscreen(self, event=None):
        self.counter = not self.counter
        self.attributes("-fullscreen", self.counter)
        return "break"

    def end_fullscreen(self, event=None):
        self.counter = False
        self.attributes("-fullscreen", False)
        return "break"


if __name__ == '__main__':
    root = Root(data=None)
    root.mainloop()