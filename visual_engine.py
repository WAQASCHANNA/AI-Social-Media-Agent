from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_social_post(base_image_path, overlay_text, brand_style):
    """
    Renders text onto the base image using brand styles.
    """
    try:
        img = Image.open(base_image_path).convert("RGB")
    except FileNotFoundError:
        # Fallback if image missing
        img = Image.new('RGB', (800, 600), color='gray')

    draw = ImageDraw.Draw(img)
    W, H = img.size

    # Load Font (fallback to default if custom not available)
    try:
        # Using a default font but scaling it up
        font_size = 40
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Wrap text
    lines = textwrap.wrap(overlay_text, width=20) # Adjust width based on font size

    # Calculate text block size
    text_height = 0
    max_text_width = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height += bbox[3] - bbox[1] + 10 # 10px line spacing
        max_text_width = max(max_text_width, text_width)

    # Center text
    y_text = (H - text_height) / 2
    
    # Draw text with brand color or white
    text_color = brand_style.get('color', '#FFFFFF')
    
    # Optional: Draw a semi-transparent box behind text for readability
    padding = 20
    box_x0 = (W - max_text_width) / 2 - padding
    box_y0 = y_text - padding
    box_x1 = (W + max_text_width) / 2 + padding
    box_y1 = y_text + text_height + padding
    
    # Draw shadow/box
    draw.rectangle([box_x0, box_y0, box_x1, box_y1], fill=(0, 0, 0, 128))

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        
        x_text = (W - line_width) / 2
        
        draw.text((x_text, y_text), line, font=font, fill=text_color)
        y_text += line_height + 10

    return img
