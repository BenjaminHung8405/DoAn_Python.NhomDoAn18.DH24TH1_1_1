"""
Modern UI Components cho Amplify
Các component với thiết kế hiện đại và hiệu ứng mượt mà
"""

import tkinter as tk
from tkinter import font as tkfont
import sys
import os

# Thêm đường dẫn để import theme
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, SPACING, PADDING, apply_hover_effect

class ModernButton(tk.Frame):
    """
    Button hiện đại với hiệu ứng hover và gradient
    """
    def __init__(self, parent, text="", icon=None, command=None, 
                 style='primary', width=None, height=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.command = command
        self.style = style
        self.is_hovered = False
        
        # Màu sắc theo style
        if style == 'primary':
            self.bg_normal = COLORS['accent_primary']
            self.bg_hover = COLORS['accent_gradient_end']
            self.fg_color = COLORS['text_primary']
        elif style == 'secondary':
            self.bg_normal = COLORS['bg_card']
            self.bg_hover = COLORS['bg_hover']
            self.fg_color = COLORS['text_secondary']
        elif style == 'ghost':
            self.bg_normal = 'transparent'
            self.bg_hover = COLORS['bg_hover']
            self.fg_color = COLORS['text_secondary']
        
        self.configure(bg=self.bg_normal, cursor='hand2')
        
        # Container cho icon và text
        container = tk.Frame(self, bg=self.bg_normal)
        container.pack(expand=True, fill='both', padx=PADDING['button']['padx'], 
                      pady=PADDING['button']['pady'])
        
        # Icon nếu có
        if icon:
            self.icon_label = tk.Label(container, image=icon, bg=self.bg_normal)
            self.icon_label.pack(side='left', padx=(0, SPACING['sm']))
            self.icon_label.bind('<Button-1>', self._on_click)
            self.icon_label.bind('<Enter>', self._on_enter)
            self.icon_label.bind('<Leave>', self._on_leave)
        
        # Text
        self.text_label = tk.Label(
            container, 
            text=text,
            bg=self.bg_normal,
            fg=self.fg_color,
            font=FONTS['button'],
            cursor='hand2'
        )
        self.text_label.pack(side='left')
        
        # Bind events
        self.bind('<Button-1>', self._on_click)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        container.bind('<Button-1>', self._on_click)
        container.bind('<Enter>', self._on_enter)
        container.bind('<Leave>', self._on_leave)
        self.text_label.bind('<Button-1>', self._on_click)
        self.text_label.bind('<Enter>', self._on_enter)
        self.text_label.bind('<Leave>', self._on_leave)
        
        # Kích thước
        if width:
            self.configure(width=width)
        if height:
            self.configure(height=height)
    
    def _on_click(self, event=None):
        if self.command:
            self.command()
    
    def _on_enter(self, event=None):
        self.is_hovered = True
        self.configure(bg=self.bg_hover)
        self.text_label.configure(
            bg=self.bg_hover,
            fg=COLORS['text_primary']
        )
        if hasattr(self, 'icon_label'):
            self.icon_label.configure(bg=self.bg_hover)
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=self.bg_hover)
    
    def _on_leave(self, event=None):
        self.is_hovered = False
        self.configure(bg=self.bg_normal)
        self.text_label.configure(
            bg=self.bg_normal,
            fg=self.fg_color
        )
        if hasattr(self, 'icon_label'):
            self.icon_label.configure(bg=self.bg_normal)
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=self.bg_normal)

class ModernCard(tk.Frame):
    """
    Card container với shadow và rounded effect
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            bg=COLORS['bg_card'],
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )
        
        # Inner padding
        self.inner = tk.Frame(self, bg=COLORS['bg_card'])
        self.inner.pack(expand=True, fill='both', 
                       padx=PADDING['card']['padx'],
                       pady=PADDING['card']['pady'])
    
    def add_content(self, widget):
        """Thêm nội dung vào card"""
        widget.pack(in_=self.inner, fill='both', expand=True)

class ModernIconButton(tk.Label):
    """
    Icon button với hiệu ứng hover đẹp
    """
    def __init__(self, parent, icon=None, text="", command=None, 
                 show_text=True, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.command = command
        self.icon = icon
        self.text_str = text
        self.show_text = show_text
        self.is_active = False
        
        # Màu sắc
        self.bg_normal = COLORS['sidebar_bg']
        self.bg_hover = COLORS['sidebar_hover']
        self.bg_active = COLORS['sidebar_active']
        self.fg_normal = COLORS['text_secondary']
        self.fg_active = COLORS['text_primary']
        
        self.configure(
            bg=self.bg_normal,
            fg=self.fg_normal,
            font=FONTS['body_md'],
            cursor='hand2',
            compound='left',
            anchor='w',
            padx=PADDING['button']['padx'],
            pady=PADDING['button']['pady']
        )
        
        if icon:
            self.configure(image=icon)
        
        if show_text:
            self.configure(text=f"  {text}")
        
        # Bind events
        self.bind('<Button-1>', self._on_click)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_click(self, event=None):
        if self.command:
            self.command()
    
    def _on_enter(self, event=None):
        if not self.is_active:
            self.configure(
                bg=self.bg_hover,
                fg=COLORS['text_primary']
            )
    
    def _on_leave(self, event=None):
        if not self.is_active:
            self.configure(
                bg=self.bg_normal,
                fg=self.fg_normal
            )
    
    def set_active(self, active=True):
        """Đặt trạng thái active"""
        self.is_active = active
        if active:
            self.configure(
                bg=self.bg_active,
                fg=self.fg_active,
                font=FONTS['button']
            )
        else:
            self.configure(
                bg=self.bg_normal,
                fg=self.fg_normal,
                font=FONTS['body_md']
            )

class ModernSearchBar(tk.Frame):
    """
    Search bar hiện đại với icon
    """
    def __init__(self, parent, placeholder="Tìm kiếm...", command=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.command = command
        self.placeholder = placeholder
        
        self.configure(
            bg=COLORS['bg_card'],
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )
        
        # Icon search
        # Note: Cần thêm icon search vào project
        
        # Entry
        self.entry = tk.Entry(
            self,
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            font=FONTS['body_md'],
            borderwidth=0,
            insertbackground=COLORS['text_primary']
        )
        self.entry.pack(side='left', fill='both', expand=True, 
                       padx=PADDING['input']['padx'],
                       pady=PADDING['input']['pady'])
        
        # Placeholder
        self.entry.insert(0, placeholder)
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<Return>', self._on_enter)
        
        # Hover effect
        self.bind('<Enter>', lambda e: self.configure(
            highlightbackground=COLORS['accent_primary']
        ))
        self.bind('<Leave>', lambda e: self.configure(
            highlightbackground=COLORS['border']
        ))
    
    def _on_focus_in(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=COLORS['text_primary'])
    
    def _on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.configure(fg=COLORS['text_secondary'])
    
    def _on_enter(self, event):
        if self.command and self.entry.get() != self.placeholder:
            self.command(self.entry.get())
    
    def get(self):
        text = self.entry.get()
        return text if text != self.placeholder else ""

class ModernDivider(tk.Frame):
    """
    Divider line đẹp
    """
    def __init__(self, parent, orientation='horizontal', **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(bg=COLORS['divider'])
        
        if orientation == 'horizontal':
            self.configure(height=1)
        else:
            self.configure(width=1)

class ModernLabel(tk.Label):
    """
    Label với typography đẹp
    """
    def __init__(self, parent, text="", size='md', weight='normal', 
                 color='primary', **kwargs):
        super().__init__(parent, **kwargs)
        
        # Font
        if weight == 'bold':
            if size == 'xl':
                font = FONTS['heading_xl']
            elif size == 'lg':
                font = FONTS['heading_lg']
            elif size == 'md':
                font = FONTS['heading_md']
            else:
                font = FONTS['heading_sm']
        else:
            if size == 'lg':
                font = FONTS['body_lg']
            elif size == 'md':
                font = FONTS['body_md']
            else:
                font = FONTS['body_sm']
        
        # Color
        if color == 'primary':
            fg = COLORS['text_primary']
        elif color == 'secondary':
            fg = COLORS['text_secondary']
        elif color == 'muted':
            fg = COLORS['text_muted']
        elif color == 'accent':
            fg = COLORS['text_accent']
        else:
            fg = color
        
        self.configure(
            text=text,
            font=font,
            fg=fg,
            bg=COLORS['bg_primary']
        )

class GradientFrame(tk.Canvas):
    """
    Frame với gradient background
    """
    def __init__(self, parent, color1=None, color2=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        if color1 is None:
            color1 = COLORS['accent_gradient_start']
        if color2 is None:
            color2 = COLORS['accent_gradient_end']
        
        self.color1 = color1
        self.color2 = color2
        
        self.configure(
            highlightthickness=0,
            borderwidth=0
        )
        
        self.bind('<Configure>', self._draw_gradient)
    
    def _draw_gradient(self, event=None):
        """Vẽ gradient"""
        self.delete('gradient')
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Tạo gradient từ trái sang phải
        limit = width
        
        # Parse colors
        r1, g1, b1 = self._hex_to_rgb(self.color1)
        r2, g2, b2 = self._hex_to_rgb(self.color2)
        
        for i in range(limit):
            ratio = i / limit
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.create_line(i, 0, i, height, fill=color, tags='gradient')
    
    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Export tất cả components
__all__ = [
    'ModernButton',
    'ModernCard',
    'ModernIconButton',
    'ModernSearchBar',
    'ModernDivider',
    'ModernLabel',
    'GradientFrame',
]
