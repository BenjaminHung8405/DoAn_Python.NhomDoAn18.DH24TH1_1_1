"""
Script to create app logo if not exists
"""
from PIL import Image, ImageDraw, ImageFont
import os


def create_app_logo():
    """Create a simple Amplify logo"""
    # Create images directory if not exists
    os.makedirs('images', exist_ok=True)
    
    # Create 64x64 logo
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw circle background (Spotify green)
    draw.ellipse([2, 2, size-2, size-2], fill='#1DB954')
    
    # Draw "A" letter
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Center the text
    text = "A"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    # Save
    img.save('images/app_64.png')
    print("✓ Created images/app_64.png")
    
    # Create larger version for loading screen
    img_large = img.resize((150, 150), Image.LANCZOS)
    img_large.save('images/loading.png')
    print("✓ Created images/loading.png")


if __name__ == '__main__':
    create_app_logo()
    print("\n✓ Logo files created successfully!")
    print("Run 'python main.py' to start the app")