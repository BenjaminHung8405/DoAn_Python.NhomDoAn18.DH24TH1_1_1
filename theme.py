"""
Theme và Style Configuration cho Amplify
Định nghĩa tất cả màu sắc, font, và style constants
"""

# ==================== MÀU SẮC ====================

# Background Colors - Gradient Dark Theme
COLORS = {
    # 1. Primary Backgrounds (Nền chính của Spotify)
    'bg_primary': '#000000',      # Nền ngoài cùng, sidebar (Đen tuyền)
    'bg_secondary': '#121212',    # Nền nội dung chính (Xám rất tối)
    'bg_card': '#181818',         # Nền thẻ (album, artist), thanh player
    'bg_hover': '#2A2A2A',        # Màu khi di chuột qua thẻ (card)
    
    # 2. Accent Colors (Màu nhấn)
    'accent_primary': '#1DB954',  # Xanh lá cây chính của Spotify
    'accent_secondary': '#FFFFFF',# Thường dùng cho các nút phụ (ví dụ: 'Sign up')
    
    # (Spotify không dùng gradient, đặt trùng màu chính để tránh lỗi)
    'accent_gradient_start': '#1DB954',
    'accent_gradient_end': '#1DB954',
    
    # 3. Text Colors (Màu văn bản)
    'text_primary': '#FFFFFF',    # Văn bản chính (Tiêu đề bài hát, v.v.)
    'text_secondary': '#B3B3B3',  # Văn bản phụ (Tên nghệ sĩ, menu không active)
    'text_muted': '#535353',      # Văn bản chìm (Thông tin phụ, sub-text)
    'text_accent': '#1DB954',     # Văn bản màu xanh lá
    
    # 4. Status Colors (Màu trạng thái)
    'success': '#1DB954',         # Dùng luôn màu xanh Spotify cho 'Thành công'
    'warning': '#FFAF36',         # Vàng (Màu cảnh báo chung)
    'error': '#F56565',           # Đỏ (Màu lỗi chung)
    'info': '#4299E1',            # Xanh dương (Màu thông tin chung)
    
    # 5. Border & Divider (Viền & Phân cách)
    'border': '#2A2A2A',          # Viền thẻ (nếu có)
    'divider': '#2A2A2A',         # Đường kẻ phân cách (subtle)
    
    # 6. Sidebar (Thanh điều hướng)
    'sidebar_bg': '#000000',      # Nền sidebar (Đen tuyền)
    'sidebar_active': '#181818',  # Nền của mục đang được chọn
    'sidebar_hover': '#181818',   # Nền khi di chuột qua mục
}

# ==================== FONTS ====================

FONTS = {
    # Headings
    'heading_xl': ('Play', 32, 'bold'),
    'heading_lg': ('Play', 24, 'bold'),
    'heading_md': ('Play', 20, 'bold'),
    'heading_sm': ('Play', 16, 'bold'),
    
    # Body text
    'body_lg': ('Play', 14),
    'body_md': ('Play', 12),
    'body_sm': ('Play', 11),
    
    # Special
    'button': ('Play', 12, 'bold'),
    'label': ('Play', 10),
    'caption': ('Play', 9),
}

# ==================== SPACING ====================

SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 12,
    'lg': 16,
    'xl': 24,
    'xxl': 32,
}

# ==================== SIZES / LAYOUT ====================
# Các kích thước tiêu chuẩn cho component và layout
SIZES = {
    'card_min_width': 160,
    'card_max_width': 220,
    'card_gap': 16,
    'content_max_width': 1200,
}

PADDING = {
    'card': {'padx': 16, 'pady': 16},
    'button': {'padx': 20, 'pady': 10},
    'input': {'padx': 12, 'pady': 8},
}

# ==================== BORDER RADIUS ====================
# Tkinter không hỗ trợ border radius trực tiếp, nhưng có thể dùng cho reference

RADIUS = {
    'sm': 4,
    'md': 8,
    'lg': 12,
    'xl': 16,
    'full': 9999,
}

# ==================== SHADOWS ====================

SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
}

# ==================== ANIMATIONS ====================

ANIMATIONS = {
    'duration_fast': 150,    # ms
    'duration_normal': 300,
    'duration_slow': 500,
}

# ==================== BUTTON STYLES ====================

BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['accent_primary'],
        'fg': COLORS['text_primary'],
        'activebackground': COLORS['accent_gradient_end'],
        'activeforeground': COLORS['text_primary'],
        'borderwidth': 0,
        'relief': 'flat',
        'cursor': 'hand2',
    },
    'secondary': {
        'bg': COLORS['bg_card'],
        'fg': COLORS['text_secondary'],
        'activebackground': COLORS['bg_hover'],
        'activeforeground': COLORS['text_primary'],
        'borderwidth': 0,
        'relief': 'flat',
        'cursor': 'hand2',
    },
    'outline': {
        'bg': 'transparent',
        'fg': COLORS['accent_primary'],
        'activebackground': COLORS['bg_hover'],
        'activeforeground': COLORS['accent_primary'],
        'borderwidth': 2,
        'relief': 'solid',
        'cursor': 'hand2',
    },
    'ghost': {
        'bg': COLORS['bg_primary'],
        'fg': COLORS['text_secondary'],
        'activebackground': COLORS['bg_hover'],
        'activeforeground': COLORS['text_primary'],
        'borderwidth': 0,
        'relief': 'flat',
        'cursor': 'hand2',
    },
}

# ==================== GRADIENT HELPER ====================

def get_gradient_colors(start_color, end_color, steps=10):
    """
    Tạo list màu gradient giữa 2 màu
    Hữu ích cho các hiệu ứng gradient
    """
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    
    gradient = []
    for i in range(steps):
        ratio = i / (steps - 1)
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
        gradient.append(rgb_to_hex((r, g, b)))
    
    return gradient

# ==================== HELPER FUNCTIONS ====================

def apply_button_style(button, style='primary'):
    """Áp dụng style cho button"""
    style_config = BUTTON_STYLES.get(style, BUTTON_STYLES['primary'])
    for key, value in style_config.items():
        try:
            button[key] = value
        except:
            pass

def apply_hover_effect(widget, enter_color=None, leave_color=None):
    """Thêm hiệu ứng hover cho widget"""
    if enter_color is None:
        enter_color = COLORS['bg_hover']
    if leave_color is None:
        leave_color = COLORS['bg_card']
    
    def on_enter(e):
        widget['background'] = enter_color
    
    def on_leave(e):
        widget['background'] = leave_color
    
    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)

def apply_card_button_style(button):
    """Style chuẩn cho Card dạng Button (ảnh + tiêu đề)"""
    try:
        button['background'] = COLORS['bg_card']
        button['activebackground'] = COLORS['bg_hover']
        button['foreground'] = COLORS['text_primary']
        button['activeforeground'] = COLORS['text_primary']
        button['relief'] = 'flat'
        button['border'] = 0
        button['borderwidth'] = 0
        button['highlightthickness'] = 1
        button['highlightbackground'] = COLORS['border']
        button['cursor'] = 'hand2'
    except:
        pass

    def on_enter(_):
        try:
            button['background'] = COLORS['bg_hover']
            button['highlightbackground'] = COLORS['accent_primary']
        except:
            pass

    def on_leave(_):
        try:
            button['background'] = COLORS['bg_card']
            button['highlightbackground'] = COLORS['border']
        except:
            pass

    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)

# ==================== EXPORT ====================

__all__ = [
    'COLORS',
    'FONTS', 
    'SPACING',
    'SIZES',
    'PADDING',
    'RADIUS',
    'SHADOWS',
    'ANIMATIONS',
    'BUTTON_STYLES',
    'get_gradient_colors',
    'apply_button_style',
    'apply_hover_effect',
    'apply_card_button_style',
]
