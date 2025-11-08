import tkinter as tk
from Base import top
from Base.bottom import Bottom
from ActivityIndicator.Activity_Indicator import ImageLabel


class Splash(tk.Toplevel):
    def __init__(self, parent, on_loading_complete):
        tk.Toplevel.__init__(self, parent)
        self.title("Splash")
        self['bg'] = 'black'
        self.on_loading_complete = on_loading_complete

        self.attributes('-fullscreen', True)

        self.lbl = ImageLabel(self)
        self.lbl['bd'] = 0
        self.lbl['bg'] = 'black'
        self.lbl.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.logo = tk.PhotoImage(file=r'images/loading.png', height=150, width=360)
        self.labelLogo = tk.Label(self, image=self.logo, bd=0, bg='black')
        self.labelLogo.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        
        # Add loading text
        self.loading_text = tk.Label(self, text="Đang tải dữ liệu ứng dụng...", 
                                   fg='white', bg='black', font=('Segoe UI', 12))
        self.loading_text.grid(row=2, column=0, pady=(10, 0))
        
        self.grid_columnconfigure(0, weight=1)
        
        # Maximize window
        try:
            self.state('zoomed')
        except:
            self.attributes('-zoomed', True)

        # Start loading animation
        self.lbl.load('ActivityIndicator/Activity.gif')
        
        # Start database preloading using after() to avoid blocking UI
        self.after(100, self._start_preload)
    
    def _start_preload(self):
        """Start database preloading in chunks to avoid blocking UI"""
        self.loading_step = 0
        self.loading_success = True
        # Ensure GIF animation is running
        if hasattr(self.lbl, 'next_frame'):
            self.lbl.next_frame()
        self._preload_next_chunk()
    
    def _preload_next_chunk(self):
        """Load next chunk of database data"""
        try:
            if self.loading_step == 0:
                # Load HomePagedata
                from Database import HomePagedata
                # Force loading of genre data
                _ = HomePagedata.genre_data
                self.loading_text.config(text="Đang tải thể loại...")
                
            elif self.loading_step == 1:
                # Load artist data
                from Database import HomePagedata
                _ = HomePagedata.artist_data
                self.loading_text.config(text="Đang tải nghệ sĩ...")
                
            elif self.loading_step == 2:
                # Load language data
                from Database import HomePagedata
                _ = HomePagedata.language_data
                self.loading_text.config(text="Đang tải ngôn ngữ...")
                
            elif self.loading_step == 3:
                # Load trending data
                from Database import HomePagedata
                _ = HomePagedata.Trending_data
                self.loading_text.config(text="Đang tải bài hát thịnh hành...")
                
            elif self.loading_step == 4:
                # Load album data
                from Database import HomePagedata
                _ = HomePagedata.album_data
                self.loading_text.config(text="Đang tải album...")
                
            elif self.loading_step == 5:
                # Load playlist data
                from Database import HomePagedata
                _ = HomePagedata.playlist_data
                self.loading_text.config(text="Đang tải danh sách phát...")
                
            elif self.loading_step == 6:
                # Load user data if available
                from user_session import UserSession
                user_data = UserSession.get_user()
                if user_data:
                    from Database.Database import get_user
                    _ = get_user(user_data['uid'])
                    self.loading_text.config(text="Đang tải hồ sơ người dùng...")
                # If no user data, skip to completion
                
            self.loading_step += 1
            
            # Schedule next chunk or complete
            if self.loading_step <= 6:
                # Restart GIF animation before next chunk
                if hasattr(self.lbl, 'next_frame'):
                    self.lbl.next_frame()
                self.after(50, self._preload_next_chunk)  # Small delay between chunks
            else:
                print("✓ Database preloading completed successfully")
                self.after(0, lambda: self._on_loading_complete(True))
                
        except Exception as e:
            print(f"⚠ Database preloading failed at step {self.loading_step}: {e}")
            self.loading_success = False
            self.after(0, lambda: self._on_loading_complete(False))
    
    def _on_loading_complete(self, success):
        """Called when loading is complete"""
        if success:
            self.loading_text.config(text="Tải hoàn tất!", fg='#48BB78')
        else:
            self.loading_text.config(text="Tải thất bại, nhưng tiếp tục...", fg='#F56565')
        
        # Restart GIF animation one final time
        if hasattr(self.lbl, 'next_frame'):
            self.lbl.next_frame()
        
        # Wait a moment to show completion message, then call callback
        self.after(1000, lambda: self.on_loading_complete(success))


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

        # Make window borderless to prevent accidental closing
        # self.overrideredirect(True)
        
        # Make window fullscreen
        self.attributes('-fullscreen', True)
        
        # Add keyboard shortcuts for closing the app
        self.bind('<Control-q>', lambda e: self.quit())
        self.bind('<Alt-F4>', lambda e: self.quit())

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        # Hide main window initially
        self.withdraw()
        
        # Show splash screen with loading callback
        self.splash = Splash(self, self.on_loading_complete)
        
        # Store data for later use
        self.user_data = data
    
    def on_loading_complete(self, success):
        """Called when database loading is complete"""
        # Create main window
        self.create_main_window()
        
        # Destroy splash screen after a short delay to ensure main window is fully rendered
        self.after(500, lambda: self._destroy_splash())
    
    def _destroy_splash(self):
        """Safely destroy splash screen"""
        try:
            if hasattr(self, 'splash') and self.splash:
                self.splash.destroy()
        except:
            pass
    
    def create_main_window(self):
        """Create the main application window after loading is complete"""
        # Setup main window
        self.title('Amplify')
        app_icon = tk.PhotoImage(file=r"images/app_64.png")
        self.iconphoto(False, app_icon)

        container = Container(self)
        container.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Maximize window
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
    # Luôn hiển thị màn hình đăng nhập - không còn phụ thuộc vào file "user"
    from Pages.UserAuthentication.AuthBase import AuthBase
    login = AuthBase()
    login.mainloop()
