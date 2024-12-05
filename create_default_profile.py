from PIL import Image, ImageDraw, ImageFont
import os

def create_default_avatar():
    # Create a new image with a gradient background
    size = (200, 200)
    img = Image.new('RGB', size, '#f0f0f0')
    draw = ImageDraw.Draw(img)

    # Draw a circular background
    margin = 10
    draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], fill='#4CAF50')

    # Draw the person silhouette
    # Head
    head_size = 60
    head_top = 45
    head_left = (size[0] - head_size) // 2
    draw.ellipse([head_left, head_top, head_left + head_size, head_top + head_size], fill='white')

    # Body
    shoulder_top = head_top + head_size - 10
    shoulder_width = 100
    shoulder_left = (size[0] - shoulder_width) // 2
    draw.ellipse([shoulder_left, shoulder_top, shoulder_left + shoulder_width, shoulder_top + 80], fill='white')

    # Save the image
    static_path = 'static'
    if not os.path.exists(static_path):
        os.makedirs(static_path)
    
    img.save('static/default_profile.png', quality=95)

if __name__ == '__main__':
    create_default_avatar()
