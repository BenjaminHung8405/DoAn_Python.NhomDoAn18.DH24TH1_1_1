import tkinter as tk
from Pages.HomePage.Home import Home
from Pages.Browse.browse import Browse
from Pages.ArtistPage.Artist import Artist
from Pages.AlbumPage.Album import Album
from tkinter import font
from PIL import ImageTk, Image
import sys
import os

# Import theme mới
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from theme import COLORS, FONTS, SPACING, PADDING
    print(f"✓ Theme loaded in topLeft.py - Sidebar BG: {COLORS['sidebar_bg']}")
except Exception as e:
    print(f"✗ Theme import failed: {e}")
    # Fallback to old colors if theme fails
    COLORS = {'sidebar_bg': '#121212', 'text_secondary': '#a8a8a8', 'sidebar_hover': '#151A3D', 
              'text_primary': '#FFFFFF', 'sidebar_active': '#1E2749', 'bg_primary': '#121212'}
    FONTS = {'body_md': ('Play', 12), 'button': ('Play', 12, 'bold')}
    SPACING = {'sm': 8, 'md': 12, 'lg': 16}
    PADDING = {'button': {'padx': 20, 'pady': 10}}


class IconButton(tk.Button):
    """Button với icon - Thiết kế hiện đại với hiệu ứng hover"""
    def __init__(self, master, controller, text, image, page, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)

        self.controller = controller
        self.page = page
        self.is_active = False

        # Áp dụng theme mới
        self['foreground'] = COLORS['text_secondary']
        self['background'] = COLORS['sidebar_bg']
        self['border'] = 0
        self['activebackground'] = COLORS['sidebar_hover']
        self['activeforeground'] = COLORS['text_primary']
        self['padx'] = PADDING['button']['padx']
        self['pady'] = PADDING['button']['pady']
        self['image'] = image
        self['compound'] = tk.LEFT
        self['text'] = f"  {text}"  # Thêm space cho đẹp
        self['anchor'] = tk.W
        self['font'] = FONTS['body_md']
        self['cursor'] = 'hand2'
        self['command'] = lambda: controller.show_frame(page)
        
        # Hiệu ứng hover mượt mà
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        """Hover effect"""
        if not self.is_active:
            self['background'] = COLORS['sidebar_hover']
            self['foreground'] = COLORS['text_primary']
    
    def _on_leave(self, event):
        """Leave hover"""
        if not self.is_active:
            self['background'] = COLORS['sidebar_bg']
            self['foreground'] = COLORS['text_secondary']
    
    def set_active(self, active=True):
        """Đặt trạng thái active"""
        self.is_active = active
        if active:
            self['background'] = COLORS['sidebar_active']
            self['foreground'] = COLORS['text_primary']
            self['font'] = FONTS['button']
        else:
            self['background'] = COLORS['sidebar_bg']
            self['foreground'] = COLORS['text_secondary']
            self['font'] = FONTS['body_md']


class NormalButton(tk.Button):
    """Button thường - Style hiện đại"""
    def __init__(self, master, text, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)

        # Áp dụng theme mới
        self['foreground'] = COLORS['text_secondary']
        self['background'] = COLORS['sidebar_bg']
        self['border'] = 0
        self['activebackground'] = COLORS['sidebar_hover']
        self['activeforeground'] = COLORS['text_primary']
        self['padx'] = PADDING['button']['padx']
        self['pady'] = PADDING['button']['pady']
        self['text'] = text
        self['anchor'] = tk.W
        self['font'] = FONTS['body_md']
        self['cursor'] = 'hand2'
        
        # Hiệu ứng hover
        self.bind('<Enter>', lambda e: self.configure(
            background=COLORS['sidebar_hover'],
            foreground=COLORS['text_primary']
        ))
        self.bind('<Leave>', lambda e: self.configure(
            background=COLORS['sidebar_bg'],
            foreground=COLORS['text_secondary']
        ))



class TopLeft(tk.Frame):
    """Sidebar trái - Thiết kế hiện đại với gradient và hiệu ứng"""
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = COLORS['sidebar_bg']
        self.master = master

        self.string1 = "Copyright "u"\u00A9 2020"

        # Font - sử dụng theme mới
        self.appHighlightFont = FONTS['button']
        self.appHighlightFont2 = FONTS['body_md']
        self.appHighlightFont3 = FONTS['body_sm']

        # Hình ảnh
        self.home_icon = tk.PhotoImage(file="images/home.png")
        self.browse_icon = tk.PhotoImage(file="images/browse2.png")
        self.menu_icon = tk.PhotoImage(file="images/menu2.png")
        self.liked_image = Image.open("images/purple_heart.png")
        self.album_image = Image.open("images/playlist.png")

        # ============= HEADER - Logo & Menu =============
        self.frame1 = tk.Frame(self, bg=COLORS['sidebar_bg'], padx=SPACING['md'], pady=SPACING['md'])
        
        # Logo hoặc menu với style đẹp
        self.menu2 = tk.Menubutton(
            self.frame1, 
            image=self.menu_icon, 
            background=COLORS['sidebar_bg'], 
            activebackground=COLORS['sidebar_hover'],
            bd=0,
            cursor='hand2'
        )
        self.menu2.menu = tk.Menu(
            self.menu2,
            tearoff=0,
            background=COLORS['bg_card'], 
            activebackground=COLORS['bg_hover'],
            foreground=COLORS['text_primary'], 
            activeforeground=COLORS['text_primary'],
            font=self.appHighlightFont2,
            bd=0
        )
        self.menu2['menu'] = self.menu2.menu
        self.menu2.menu.add_command(label='AMPLIFY')
        self.menu2.menu.add_command(label=self.string1)
        self.menu2.menu.add_command(label='Contact us:')
        self.menu2.menu.add_command(label='amplifyteam1234@gmail.com')

        # ============= NAVIGATION =============
        self.frame2 = tk.Frame(self, bg=COLORS['sidebar_bg'], padx=SPACING['sm'])
        
        self.home = IconButton(
            self.frame2, 
            master, 
            text='Home', 
            image=self.home_icon, 
            page=Home
        )
        self.browse = IconButton(
            self.frame2, 
            master, 
            text='About Us', 
            image=self.browse_icon, 
            page=Browse
        )

        # ============= YOUR LIBRARY =============
        self.frame3 = tk.Frame(self, bg=COLORS['sidebar_bg'], padx=SPACING['sm'])
        
        # Header label với style đẹp
        self.label = tk.Label(
            self.frame3,
            text='YOUR LIBRARY',
            background=COLORS['sidebar_bg'],
            foreground=COLORS['text_muted'],
            anchor=tk.W,
            padx=SPACING['md'],
            pady=SPACING['sm'],
            font=FONTS['caption']
        )
        
        # Library buttons
        self.likedSongs = NormalButton(
            self.frame3,
            text='❤️  Liked Songs',
            command=lambda data=self.get_liked_song(): self.master.show_frame_liked(
                data=self.get_liked_song(),
                text='Liked Song',
                image=self.liked_image
            )
        )
        self.likedAlbums = NormalButton(
            self.frame3,
            text='💿  Liked Albums',
            command=lambda data=self.get_liked_albums(): self.master.show_frame_liked_albums(
                data=self.get_liked_albums(),
                text='Liked Album',
                image=self.album_image
            )
        )
        self.albums = NormalButton(
            self.frame3,
            text='💿  Albums',
            command=lambda: self.master.show_frame(Album)
        )
        self.artists = NormalButton(
            self.frame3,
            text='🎤  Artists',
            command=lambda: self.master.show_frame(Artist)
        )

        # ============= DIVIDER (đường phân cách đẹp) =============
        self.line = tk.Frame(self, bg=COLORS['divider'], height=1)

        # ============= FOOTER - Info =============
        self.frame4 = tk.Frame(self, bg=COLORS['sidebar_bg'], padx=SPACING['md'], pady=SPACING['sm'])
        
        self.label2 = tk.Label(
            self.frame4,
            text='🎵 AMPLIFY',
            background=COLORS['sidebar_bg'],
            foreground=COLORS['text_muted'],
            anchor=tk.W,
            font=FONTS['caption']
        )
        self.copyright = tk.Label(
            self.frame4,
            text=self.string1,
            background=COLORS['sidebar_bg'],
            foreground=COLORS['text_muted'],
            anchor=tk.W,
            font=FONTS['caption']
        )
        
        # ============= CONTACT INFO =============
        self.frame5 = tk.Frame(self, bg=COLORS['sidebar_bg'], padx=SPACING['md'], pady=SPACING['sm'])
        
        self.label4 = tk.Label(
            self.frame5,
            text='📧 CONTACT US',
            background=COLORS['sidebar_bg'],
            foreground=COLORS['text_muted'],
            anchor=tk.W,
            font=FONTS['caption']
        )
        self.label3 = tk.Label(
            self.frame5,
            text='amplifyteam1234@gmail.com',
            background=COLORS['sidebar_bg'],
            foreground=COLORS['text_accent'],
            anchor=tk.W,
            font=FONTS['caption'],
            cursor='hand2'
        )
        # Hover effect cho email
        self.label3.bind('<Enter>', lambda e: self.label3.configure(
            foreground=COLORS['accent_primary']
        ))
        self.label3.bind('<Leave>', lambda e: self.label3.configure(
            foreground=COLORS['text_accent']
        ))

        # ============= GRID LAYOUT =============
        # Components
        self.menu2.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.home.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=2)
        self.browse.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=2)
        self.label.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.likedSongs.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=2)
        self.likedAlbums.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=2)
        self.albums.grid(row=3, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=2)
        self.artists.grid(row=4, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=2)
        self.copyright.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=2)        
        self.label2.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=2)
        self.label3.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=2)
        self.label4.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=2)

        # Frames
        self.frame1.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.frame2.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=SPACING['sm'])
        self.frame3.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=SPACING['sm'])
        self.line.grid(row=3, column=0, sticky=tk.E + tk.W, pady=SPACING['lg'])
        self.frame4.grid(row=4, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.frame5.grid(row=5, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=9)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.frame5.grid_columnconfigure(0, weight=1)
        self.frame5.grid_rowconfigure((0,1), weight=1)

    def logout(self):
        import os
        from Database.Database import sign_out
        from Pages.UserAuthentication.AuthBase import AuthBase
        sign_out()
       
        self.master.master.master.destroy()
        login = AuthBase()
        login.mainloop()

    def get_liked_song(self):
        # Lấy user_id từ session thay vì file
        from user_session import UserSession
        user_id = UserSession.get_user_id()
        if not user_id:
            return []  # Trả về danh sách rỗng nếu không có user
            
        from Database.Database import get_all_liked_songs
        return get_all_liked_songs(user_id)

    def get_liked_albums(self):
        # Lấy user_id từ session thay vì file
        from user_session import UserSession
        user_id = UserSession.get_user_id()
        if not user_id:
            return []  # Trả về danh sách rỗng nếu không có user
            
        from Database.Database import get_user_liked_albums, get_album
        liked_albums = get_user_liked_albums(user_id)
        
        # Chuyển đổi format để tương thích với show_frame_liked
        album_data = []
        for album in liked_albums:
            # Load tracks cho album
            tracks = get_album(album_name=album['title'])
            album_dict = {
                'album_id': album['album_id'],
                'text': album['title'],
                'url': album['cover_image_url'] or '',
                'tracks': tracks if tracks else []
            }
            album_data.append(album_dict)
        
        return album_data

