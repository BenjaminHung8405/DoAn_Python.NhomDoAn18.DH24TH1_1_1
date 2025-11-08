import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
from .listOfPage import pages, rightPage, incrementCount, getCount, resetCount
from Pages.UserPage.UserPage import UserPage
import sys
import subprocess
import os

# Import theme mới
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, SPACING, PADDING


class UserEntry(tk.Entry):
    """Search bar với thiết kế hiện đại"""
    def __init__(self, master, placeholder, textvariable, songDict, *args, **kwargs):
        tk.Entry.__init__(self, master, *args, **kwargs)

        # Hàm placeholder
        def default_placeholder(self):
            self.insert(0, placeholder)

        default_placeholder(self)

        # Áp dụng theme mới - Search bar đẹp
        self['background'] = COLORS['bg_card']
        self['foreground'] = COLORS['text_secondary']
        self['insertbackground'] = COLORS['text_primary']
        self['font'] = FONTS['body_md']
        self['border'] = 0
        self['relief'] = 'flat'
        
        # Padding đẹp hơn
        self.default_fg = COLORS['text_secondary']
        self.input_fg = COLORS['text_primary']

        # Hàm được gọi khi focus
        def foc_in(event):
            if self.get() == placeholder:
                self.delete(0, 100)
            self['foreground'] = self.input_fg
            self['background'] = COLORS['bg_hover']
            self['textvariable'] = textvariable

        # Hàm được gọi khi không focus
        def foc_out(event):
            self['background'] = COLORS['bg_card']
            self['foreground'] = self.default_fg
            if not self.get():
                default_placeholder(self)
            else:
                self.insert(0, self['textvariable'])

        self.bind("<FocusIn>", lambda e: foc_in(e))
        self.bind("<FocusOut>", lambda e: foc_out(e))


class IconButton(tk.Button):
    """User button với style hiện đại"""
    def __init__(self, master, controller, text, image, command, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)

        # Áp dụng theme mới
        self['foreground'] = COLORS['text_primary']
        self['background'] = COLORS['bg_card']
        self['border'] = 0
        self['activebackground'] = COLORS['bg_hover']
        self['activeforeground'] = COLORS['text_primary']
        self['padx'] = PADDING['button']['padx']
        self['pady'] = PADDING['button']['pady']
        self['image'] = image
        self['compound'] = tk.LEFT
        self['text'] = f"  {text}"
        self['anchor'] = tk.W
        self['font'] = FONTS['button']
        self['command'] = command
        self['cursor'] = 'hand2'
        self['relief'] = 'flat'


class TopRightTop(tk.Frame):
    """Top bar - Navigation, search, user menu với theme hiện đại"""
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = COLORS['bg_primary']
        self['height'] = 1

        # Lấy thông tin user từ session thay vì file
        from user_session import UserSession
        user_data = UserSession.get_user()
        if not user_data:
            return  # Không thể hiển thị nếu không có user
            
        from Database.Database import get_user
        myobject = get_user(user_data['uid'])

        self.back = Back(self)
        self.search = tk.Frame(self, bg=COLORS['bg_primary'])
        self.name = tk.Frame(self, bg=COLORS['bg_primary'])
        self.min_max_cross = MinMaxCross(self)

        # Search bar với style đẹp và bo góc
        search_container = tk.Frame(self.search, bg=COLORS['bg_primary'])
        search_container.pack(fill='both', expand=True, padx=SPACING['md'], pady=SPACING['sm'])
        
        self.filter = UserEntry(
            search_container, 
            placeholder="🔍  Tìm kiếm bài hát, nghệ sĩ...",
            textvariable=None,
            songDict=None,
        )
        self.filter.pack(fill='both', expand=True, ipady=SPACING['sm'])
        self.filter.bind("<Return>", lambda e: self.sendSearchData(e))

        # User button với style mới
        self.appHighlightFont = FONTS['button']
        self.appHighlightFont2 = font.Font(family='Segoe UI', underline=1, size=12, weight='bold')
        self.user_icon = tk.PhotoImage(file="images/user2.png", height=25, width=25)
        
        self.userButton = IconButton(
            self.name,
            master, 
            text=myobject['display_name'],
            image=self.user_icon,
            command=lambda: self.master.master.show_frame(UserPage)
        )
        self.userButton.bind("<Enter>", lambda e: self.userButtonHighlight(e))
        self.userButton.bind("<Leave>", lambda e: self.userButtonLeave(e))

        # Menu thả xuống với style đẹp
        self.down = tk.PhotoImage(file="images/down_arrow.png", width=25, height=25)
        self.user_menu = tk.Menubutton(
            self.name,
            image=self.down,
            background=COLORS['bg_primary'],
            activebackground=COLORS['bg_hover'],
            bd=0, 
            padx=2, 
            pady=0,
            cursor='hand2'
        )
        self.user_menu.menu = tk.Menu(
            self.user_menu,
            tearoff=0,
            background=COLORS['bg_card'], 
            activebackground=COLORS['bg_hover'],
            foreground=COLORS['text_primary'], 
            activeforeground=COLORS['text_primary'],
            bd=0,
            font=FONTS['body_md']
        )
        self.user_menu['menu'] = self.user_menu.menu
        self.user_menu.menu.add_command(label='🚪 Logout', command=self.logout)
        self.user_menu.menu.add_command(label="👤 Profile", command=lambda: self.master.master.show_frame(UserPage))

        self.user_menu.grid(row=0, column=2, sticky='nsew', padx=SPACING['sm'], pady=0)
        self.userButton.grid(row=0, column=1, sticky='nsew', ipady=0)
        self.back.grid(row=0, column=0, sticky='nsew')
        self.search.grid(row=0, column=1, sticky='nsew')
        self.name.grid(row=0, column=2, sticky='nsew')
        self.min_max_cross.grid(row=0, column=3, sticky='nsew')

        self.search.grid_rowconfigure(0, weight=1)

        self.name.grid_rowconfigure(0, weight=1)
        self.name.grid_columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_columnconfigure(2, weight=5)
        self.grid_columnconfigure(3, weight=4)
        self.grid_propagate(False)
    
    def sendSearchData(self, event):
        self.master.focus()
        self.master.master.show_frame_Search(data=self.filter.get())

    def userButtonHighlight(self, event):
        self.userButton['bg'] = COLORS['bg_hover']
        self.userButton['font'] = self.appHighlightFont2

    def userButtonLeave(self, event):
        self.userButton['bg'] = COLORS['bg_card']
        self.userButton['font'] = self.appHighlightFont

    def logout(self):
        from Database.Database import sign_out
        sign_out()
        try:
            from Base.listOfPage import current_playing
            from Base.listOfPage import currentTrack
            if currentTrack[0]['instance'].player.music.get_busy():
                currentTrack[0]['instance'].player.music.stop()
        except Exception:
            pass
        self.master.master.master.master.destroy()
        import subprocess
        import sys
        # Use current Python interpreter instead of hardcoded path
        _ = subprocess.call([sys.executable, "main.py"])


class Back(tk.Frame):
    """Navigation buttons với theme hiện đại"""
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = COLORS['bg_primary']

        self.leftImage = tk.PhotoImage(file=r'./images/left_arrow.png')
        self.rightImage = tk.PhotoImage(file=r'./images/right_arrow.png')

        self.left = ArrowButton(self, image=self.leftImage, command=self.left)
        self.right = ArrowButton(self, image=self.rightImage, command=self.right)

        self.left.grid(row=0, column=0, sticky='ew', padx=2)
        self.right.grid(row=0, column=1, sticky='ew', padx=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

    def left(self):
        if len(pages) > 0:
            if len(pages) == 1:
                return
            else:
                r = pages.pop(len(pages) - 1)
                rightPage.append(r)
                frame = pages[len(pages) - 1]
                self.master.master.master.show_frame_directly(frame)

    def right(self):
        if len(rightPage) < 1:
            return
        c = getCount() 
        if c > len(rightPage):
            return
        frame = rightPage[len(rightPage) - c]
        pages.append(frame)
        incrementCount()
        self.master.master.master.show_frame_directly(frame)


class ArrowButton(tk.Button):
    """Arrow buttons với hiệu ứng hover"""
    def __init__(self, master, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)
        self['relief'] = tk.FLAT
        self['background'] = COLORS['bg_card']
        self['foreground'] = COLORS['text_primary']
        self['activebackground'] = COLORS['bg_hover']
        self['activeforeground'] = COLORS['text_primary']
        self['borderwidth'] = 0
        self['cursor'] = 'hand2'
        
        # Hover effects
        self.bind('<Enter>', lambda e: self.configure(background=COLORS['bg_hover']))
        self.bind('<Leave>', lambda e: self.configure(background=COLORS['bg_card']))


class MinMaxCross(tk.Frame):
    """Window controls với theme hiện đại"""
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = COLORS['bg_primary']

        self.min_icon = self.prepare_icon('min.png', 13)
        self.max_icon = self.prepare_icon('max.png', 14)
        self.cross_icon = self.prepare_icon('cross.png', 25)
        
        self.min = tk.Button(
            self,
            bg=COLORS['bg_primary'],
            activebackground=COLORS['bg_hover'],
            height=25,
            width=35,
            image=self.min_icon,
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            command=lambda: self.master.master.master.master.master.wm_state("iconic")
        )
        self.max = tk.Button(
            self,
            image=self.max_icon,
            bg=COLORS['bg_primary'],
            relief=tk.FLAT,
            height=25,
            width=35,
            bd=0,
            cursor='hand2',
            activebackground=COLORS['bg_hover'],
            command=lambda: self.master.master.master.master.master.state('zoomed')
        )
        self.cross = tk.Button(
            self,
            bg=COLORS['bg_primary'],
            activebackground=COLORS['error'],
            image=self.cross_icon,
            relief=tk.FLAT,
            width=35,
            bd=0,
            cursor='hand2',
            command=lambda: sys.exit()
        )
        
        self.min.grid(row=0, column=1)
        self.max.grid(row=0, column=2)
        self.cross.grid(row=0, column=3)

        self.min.bind('<Enter>', self.enter)
        self.min.bind('<Leave>', self.leave)
        self.max.bind('<Enter>', self.max_enter)
        self.max.bind('<Leave>', self.max_leave)
        self.cross.bind('<Enter>', self.cross_enter)
        self.cross.bind('<Leave>', self.cross_leave)

        self.grid_columnconfigure(0, weight=1)

    def enter(self, event):
        self.min.config(bg=COLORS['bg_hover'])

    def leave(self, event):
        self.min.config(bg=COLORS['bg_primary'])

    def max_enter(self, event):
        self.max.config(bg=COLORS['bg_hover'])

    def max_leave(self, event):
        self.max.config(bg=COLORS['bg_primary'])

    def cross_enter(self, event):
        self.cross.config(bg=COLORS['error'])

    def cross_leave(self, event):
        self.cross.config(bg=COLORS['bg_primary'])

    @staticmethod
    def prepare_icon(filename, size):
        icon = Image.open('images/' + filename)
        icon = icon.resize((size, size), Image.LANCZOS)
        icon = ImageTk.PhotoImage(icon)
        return icon
