from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import matplotlib.pyplot as plt

class FlowerCanvas:
    def __init__(self, canvas_width=400, canvas_height=300, img_size=(200, 200)):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.img_size = img_size

    def draw_flower_canvas(self, flower):
        # Load the image from the URL
        response = requests.get(flower['image_url'])
        img = Image.open(BytesIO(response.content))

        # Resize the image
        img = img.resize(self.img_size)

        # Create a new image for the canvas
        canvas = Image.new('RGB', (self.canvas_width, self.canvas_height), (255, 255, 255))

        # Paste the flower image onto the canvas
        img_x = (self.canvas_width - self.img_size[0]) // 2
        canvas.paste(img, (img_x, 20))

        # Draw text (flower name and ID) below the image
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.load_default()

        text = f"Name: {flower['name']}\nID: {flower['flower_id']}"
        text_x = 50
        text_y = self.img_size[1] + 40
        draw.text((text_x, text_y), text, fill="black", font=font)

        return canvas

    def show_flower_canvas(self, flowers):
        num_flowers = len(flowers)
        fig, axes = plt.subplots(1, num_flowers, figsize=(self.canvas_width/100*num_flowers, self.canvas_height/100))

        if num_flowers == 1:
            axes = [axes]

        for ax, flower in zip(axes, flowers):
            canvas = self.draw_flower_canvas(flower)
            ax.imshow(canvas)
            ax.axis('off')

        plt.show()