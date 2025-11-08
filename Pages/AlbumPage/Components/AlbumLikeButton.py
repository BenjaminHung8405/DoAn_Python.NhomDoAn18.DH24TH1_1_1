import tkinter as tk
from PIL import Image, ImageTk


class AlbumLikeButton(tk.Button):
    def __init__(self, master, album_id, album_title, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)

        self.album_id = album_id
        self.album_title = album_title
        self.liked = False

        self.empty_heart = self.prepare_image('empty_heart.png', 20)
        self.filled_heart = self.prepare_image('filled_heart.png', 20)

        self['background'] = '#181818'
        self['activebackground'] = '#333333'
        self['bd'] = 0
        self['image'] = self.empty_heart
        self['command'] = self.clicked

        # Check if user has liked this album
        from user_session import UserSession
        user_id = UserSession.get_user_id()
        if user_id:
            from Database.Database import is_album_liked
            if is_album_liked(user_id, self.album_id):
                self.liked = True
                self['image'] = self.filled_heart

    def clicked(self):
        from user_session import UserSession
        user_id = UserSession.get_user_id()
        if not user_id:
            return  # Cannot perform action without user

        if self.liked:
            # Unlike
            self['image'] = self.empty_heart
            self.liked = False
            from Database.Database import unlike_album
            unlike_album(user_id, self.album_id)
        else:
            # Like
            self['image'] = self.filled_heart
            self.liked = True
            from Database.Database import like_album
            like_album(user_id, self.album_id)

    @staticmethod
    def prepare_image(filename, size):
        icon = Image.open('images/'+filename)
        icon = icon.resize((size, size), Image.LANCZOS)
        icon = ImageTk.PhotoImage(icon)
        return icon