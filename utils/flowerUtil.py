from PIL import Image
import cv2
import requests
from collections import Counter
from matplotlib.colors import to_hex, rgb_to_hsv
from io import BytesIO
import numpy as np
import os 

current_directory = os.path.dirname(__file__)
DEPLOY_FILE_PATH = os.path.join(current_directory, 'deploy.prototxt')
MODEL_FILE_PATH = os.path.join(current_directory, 'hed_pretrained_bsds.caffemodel')

# Contains methods used to calculate various information on a flower image. 
class FlowerUtil:
    def __init__(self):
        pass

    # Gets the most used colors in a flower image, specifically around the flower. 
    def get_top_colors(self, image_url: str, num_colors: int = 5):
        img_rgb = self.flower_outline_detect(image_url)
        if img_rgb is None:
            return None, None

        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.convert('RGB')
        img_pil = img_pil.resize((100, 100))

        pixels = img_pil.getdata()
        color_counts = Counter(pixels)
        top_colors = color_counts.most_common(num_colors)

        hsv_values = []
        for color, count in top_colors:
            hex_color = to_hex([x/255.0 for x in color])
            hsv_color = rgb_to_hsv([x/255.0 for x in color])
            hue = hsv_color[0] * 360
            saturation = hsv_color[1] * 100
            value = hsv_color[2] * 100
            hsv_values.append((hue, saturation, value))

        return top_colors, hsv_values
    
    # Converts any hex code to HSV. 
    def hex_to_hsv(self, hex_color):
        rgb = [int(hex_color[i:i+2], 16) / 255.0 for i in (1, 3, 5)]
        return rgb_to_hsv(rgb)
    
    # Creates a contour around the flower using edge detection. 
    def flower_outline_detect(self, image_url: str):
        response = requests.get(image_url)
        img_array = np.frombuffer(response.content, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        blr = cv2.GaussianBlur(img_rgb, (9, 9), 0)


        (H, W) = img_rgb.shape[:2] 
        blob = cv2.dnn.blobFromImage(blr, scalefactor=1.0, size=(W, H), 
                                    swapRB=False, crop=False) 
        net = cv2.dnn.readNetFromCaffe(DEPLOY_FILE_PATH, MODEL_FILE_PATH) 
        net.setInput(blob) 
        hed = net.forward() 
        hed = cv2.resize(hed[0, 0], (W, H)) 
        hed = (255 * hed).astype("uint8") 
        
        # Thresholding to create a binary image
        _, binary_hed = cv2.threshold(hed, 85, 255, cv2.THRESH_BINARY)
        
        # Finding contours
        contours, _ = cv2.findContours(binary_hed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(len(contours))
        # Filter out small contours (optional)
        min_contour_area = 1000  # Adjust as needed
        contours = [c for c in contours if cv2.contourArea(c) > min_contour_area]
        
        if len(contours) == 0:
            print("No contours found.")
            return None
        
        # Finding the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Create a bounding rectangle around the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(img_rgb, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Blue rectangle with thickness 2
        
        # Optionally display the images
        cv2.imshow("HED", hed)
        cv2.imshow("Largest Contour with Bounding Box", img_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return img_rgb

'''
u = FlowerUtil()
top_colors, hsv_values = u.get_top_colors('https://storage.googleapis.com/flower-db-prd/da135b925febb70955ddf7e4d7e1eac6.jpg')
print("Top Colors:", top_colors)
print("HSV Values:", hsv_values)
'''