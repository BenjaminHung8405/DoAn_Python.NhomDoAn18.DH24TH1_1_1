import tkinter as tk
from PIL import Image, ImageTk


class LikeButton(tk.Button):
    def __init__(self, master, *args, **kwargs):
        self.title = kwargs.pop('title')
        self.album = kwargs.pop('album')
        self.url = kwargs.pop('url')
        self.artist = kwargs.pop('artist')
        tk.Button.__init__(self, master, *args, **kwargs)

        self.liked = True

        self.empty_heart = self.prepare_image('empty_heart.png', 16)
        self.filled_heart = self.prepare_image('filled_heart.png', 16)

        self['background'] = '#181818'
        self['activebackground'] = '#333333'
        self['bd'] = 0
        self['image'] = self.empty_heart
        self['command'] = self.clicked
        # Lấy user_id từ session thay vì file
        from user_session import UserSession
        user_id = UserSession.get_user_id()
        if user_id:
            from Database.Database import get_all_liked_songs
            for index, song in enumerate(get_all_liked_songs(user_id)):
                for key, value in song.items():
                    if key == 'title' and value == self.title:
                        self.liked = False
                        self['image'] = self.filled_heart

        # self.bind('<Button-1>', self.master.master.click)

    def clicked(self):
        # Lấy user_id từ session thay vì file
        from user_session import UserSession
        user_id = UserSession.get_user_id()
        if not user_id:
            return  # Không thể thực hiện nếu không có user
            
        from Base.listOfPage import likedSong
        if not self.liked:
            # if unliked
            self['image'] = self.empty_heart
            self.liked = True
           
            from Database.Database import delete_liked_song
            delete_liked_song(user_id , self.title)
                
            
            return
        # if liked
        self['image'] = self.filled_heart
        self.liked = False
        from Database.Database import add_liked_songs
        track_object = {
            'title': self.title,
            'genre': self.album,
            'artist': self.artist,
            'location': self.url
        }
        
        add_liked_songs(track_object, user_id)
        likedSong.append(track_object)


    @staticmethod
    def prepare_image(filename, size):
        icon = Image.open('images/'+filename)
        icon = icon.resize((size, size), Image.LANCZOS)
        icon = ImageTk.PhotoImage(icon)
        return icon
