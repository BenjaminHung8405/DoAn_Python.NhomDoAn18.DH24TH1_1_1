"""
Theme và Style Configuration cho Amplify
Định nghĩa tất cả màu sắc, font, và style constants
"""

# ==================== MÀU SẮC ====================

# Background Colors - Gradient Dark Theme
COLORS = {
    # Primary Background
    'bg_primary': '#0A0E27',      # Navy blue dark - nền chính
    'bg_secondary': '#151A3D',    # Lighter navy - nền phụ
    'bg_card': '#1E2749',         # Card background
    'bg_hover': '#2A3254',        # Hover state
    
    # Accent Colors
    'accent_primary': '#6C63FF',  # Purple - màu chính
    'accent_secondary': '#4ECDC4', # Teal - màu phụ
    'accent_gradient_start': '#667EEA',
    'accent_gradient_end': '#764BA2',
    
    # Text Colors
    'text_primary': '#FFFFFF',    # White - text chính
    'text_secondary': '#A0AEC0',  # Gray - text phụ
    'text_muted': '#718096',      # Muted gray
    'text_accent': '#6C63FF',     # Purple text
    
    # Status Colors
    'success': '#48BB78',         # Green
    'warning': '#ECC94B',         # Yellow
    'error': '#F56565',           # Red
    'info': '#4299E1',            # Blue
    
    # Border & Divider
    'border': '#2D3748',
    'divider': '#1A202C',
    
    # Sidebar
    'sidebar_bg': '#0D1224',
    'sidebar_active': '#1E2749',
    'sidebar_hover': '#151A3D',
}

# ==================== FONTS ====================

FONTS = {
    # Headings
    'heading_xl': ('Segoe UI', 32, 'bold'),
    'heading_lg': ('Segoe UI', 24, 'bold'),
    'heading_md': ('Segoe UI', 20, 'bold'),
    'heading_sm': ('Segoe UI', 16, 'bold'),
    
    # Body text
    'body_lg': ('Segoe UI', 14),
    'body_md': ('Segoe UI', 12),
    'body_sm': ('Segoe UI', 11),
    
    # Special
    'button': ('Segoe UI', 12, 'bold'),
    'label': ('Segoe UI', 10),
    'caption': ('Segoe UI', 9),
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

# ==================== EXPORT ====================

__all__ = [
    'COLORS',
    'FONTS', 
    'SPACING',
    'PADDING',
    'RADIUS',
    'SHADOWS',
    'ANIMATIONS',
    'BUTTON_STYLES',
    'get_gradient_colors',
    'apply_button_style',
    'apply_hover_effect',
]
