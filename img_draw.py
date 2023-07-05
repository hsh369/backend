import requests
from PIL import Image, ImageDraw
from io import BytesIO

def draw_borders_on_image(image_url, coordinates):
    # Download the image from the URL
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    
    # Create a drawing object
    draw = ImageDraw.Draw(image)
    
    width, height = image.size
    
    # Draw borders on the image based on the given coordinates
    for xmin, xmax, ymin, ymax in coordinates:
        draw.rectangle([(xmin*width, ymin*height), (xmax*width, ymax*height)], outline='red', width=7)
    
    # Show the modified image
    image.save("media/image_with_borders.jpg")
    return "media/image_with_borders.jpg"
