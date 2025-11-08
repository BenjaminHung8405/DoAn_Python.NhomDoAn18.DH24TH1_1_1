import tkinter as tk
import pyglet
import tkinter.font as tkfont
import tkinter as tk
import pyglet
import tkinter.font as tkfont
from Pages.Resource.HorizontalScrollableFrame import HorizontalScrollableFrame
from PIL import ImageTk, Image
import requests
from io import BytesIO
from theme import COLORS, SPACING, SIZES, apply_card_button_style

# Global sizing cache
_card_target_width = 200
_container_width = 1000

def wid():
    return _card_target_width

class HorizontalFrame(tk.Frame):
    """Section gồm tiêu đề + vùng card scroll ngang."""
    def __init__(self, master, controller, data, text, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        self.data = data
        self.section_title = text
        self.configure(background=COLORS['bg_secondary'])
        self['padx'] = SPACING['xl']
        self['pady'] = SPACING['lg']

        self.header = Upper(self, self.section_title, self.data)
        self.divider = tk.Frame(self, height=1, background=COLORS['border'])
        self.content = Lower(self, controller, data)

        self.header.grid(row=0, column=0, sticky='we')
        self.divider.grid(row=1, column=0, sticky='we', pady=(SPACING['sm'], SPACING['md']))
        self.content.grid(row=2, column=0, sticky='nwe')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def right(self):
        self.content.scrollable.right()

    def left(self):
        self.content.scrollable.left()

class Upper(tk.Frame):
    def __init__(self, master, text, data, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(background=COLORS['bg_secondary'])
        pyglet.font.add_file('fonts/Play/Play-Bold.ttf')
        heading_font = tkfont.Font(family='Play', size=18, weight='bold')
        self.label = tk.Label(self, text=text, font=heading_font, anchor='w',
                              background=COLORS['bg_secondary'], foreground=COLORS['text_primary'])
        self.label.grid(row=0, column=0, sticky='w')
        if len(data) > 5:
            nav = tk.Frame(self, background=COLORS['bg_secondary'])
            nav.grid(row=0, column=1, sticky='e')
            left_icon = tk.PhotoImage(file=r'./images/left_arrow.png')
            right_icon = tk.PhotoImage(file=r'./images/right_arrow.png')
            ArrowButton(nav, image=left_icon, command=master.left).grid(row=0, column=0, padx=(0, SPACING['xs']))
            ArrowButton(nav, image=right_icon, command=master.right).grid(row=0, column=1)
            # Keep refs
            self.left_icon = left_icon
            self.right_icon = right_icon
        self.grid_columnconfigure(0, weight=1)

class Lower(tk.Frame):
    count = 0
    def __init__(self, master, controller, data, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        from Base.listOfPage import musicPages
        musicPages.append([])
        self.configure(background=COLORS['bg_secondary'])
        self['pady'] = SPACING['md']
        self.bind('<Configure>', self._on_resize)
        self.scrollable = HorizontalScrollableFrame(self)
        self.frame = tk.Frame(self.scrollable.scrollable_frame, bg=COLORS['bg_secondary'])
        self.scrollable.grid(row=0, column=0, sticky='we')
        self.frame.grid(row=0, column=0, sticky='w')
        self.images = []
        # Load images
        for item in data:
            img = self._load_image(item)
            self.images.append(img)
        for idx, item in enumerate(data):
            musicPages[Lower.count].append(0)
            img = self.images[idx] if idx < len(self.images) else None
            btn = CardButton(self.frame, text=item['text'], url=img,
                             command=lambda d=item['tracks'], im=img, txt=item['text'], r=Lower.count, c=idx: controller.show_frame_Main(
                                 data=d, image=im, text=txt, r=r, c=c))
            btn.grid(row=0, column=idx, padx=(0, SPACING['sm']))
        self.grid_columnconfigure(0, weight=1)
        Lower.count += 1

    def _load_image(self, item):
        url = item.get('url')
        if not url:
            return None
        try:
            response = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code != 200:
                return None
            if not response.headers.get('content-type', '').lower().startswith('image/'):
                return None
            data = BytesIO(response.content)
            img = Image.open(data)
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            return img
        except Exception:
            return None

    def _on_resize(self, event):
        global _container_width, _card_target_width
        _container_width = event.width
        raw = event.width / 5 - (SIZES['card_gap'] - 2)
        _card_target_width = max(SIZES['card_min_width'], min(SIZES['card_max_width'], raw))

class ArrowButton(tk.Button):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(relief='flat', background=COLORS['bg_secondary'], foreground=COLORS['text_primary'],
                       activebackground=COLORS['bg_hover'], activeforeground=COLORS['text_primary'], borderwidth=0,
                       cursor='hand2')

class CardButton(tk.Button):
    def __init__(self, master, url, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.url = url
        pyglet.font.add_file('fonts/Play/Play-Bold.ttf')
        font_play = tkfont.Font(family='Play', size=13, weight='bold')
        self.configure(height=300, border=0, font=font_play, compound='top', wraplength=SIZES['card_max_width'], justify='center')
        apply_card_button_style(self)
        self.bind('<Configure>', self._resize)
        self.bind('<Enter>', self._hover_in)
        self.bind('<Leave>', self._hover_out)

    def _get_size(self):
        raw = _container_width / 5 - (SIZES['card_gap'] - 2)
        return max(SIZES['card_min_width'], min(SIZES['card_max_width'], raw))

    def _resize(self, _):
        if self.url is None:
            return
        w = self._get_size()
        self.configure(width=int(round(w)), height=int(round(w)) + SPACING['xl'])
        resample = getattr(getattr(Image, 'Resampling', Image), 'LANCZOS', getattr(Image, 'ANTIALIAS', Image.NEAREST))
        img = self.url.resize((int(round(w)), int(round(w))), resample)
        self.image = ImageTk.PhotoImage(img)
        self.config(image=self.image)

    def _hover_in(self, _):
        if self.url is None:
            return
        w = self._get_size()
        self.configure(width=int(round(w)), height=int(round(w)) + SPACING['xl'])
        resample = getattr(getattr(Image, 'Resampling', Image), 'LANCZOS', getattr(Image, 'ANTIALIAS', Image.NEAREST))
        img = self.url.resize((int(round(w))+3, int(round(w))+3), resample)
        self.image = ImageTk.PhotoImage(img)
        self.config(image=self.image)

    def _hover_out(self, _):
        self._resize(_)

