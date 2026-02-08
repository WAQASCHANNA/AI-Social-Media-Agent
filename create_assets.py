from PIL import Image, ImageDraw
import os

def create_placeholder(path, text, color):
    img = Image.new('RGB', (800, 600), color=color)
    d = ImageDraw.Draw(img)
    d.text((10,10), text, fill=(255,255,255))
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print(f"Created {path}")

if __name__ == "__main__":
    assets = [
        ("assets/confetti.png", "Confetti Background", "purple"),
        ("assets/gradient_bg.png", "Gradient Background", "blue"),
        ("assets/product_shot.png", "Product Mockup", "teal"),
        ("assets/meme_bg.png", "Meme Background", "orange"),
        ("assets/chart_bg.png", "Data Chart Background", "black")
    ]
    
    for path, text, color in assets:
        create_placeholder(path, text, color)
