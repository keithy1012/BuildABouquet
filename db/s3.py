import requests
from PIL import Image
import numpy as np
import json
import io
import boto3
from dotenv import load_dotenv
import os

# Stores flower names, images as np.array, and month in AWS S3. 
class S3Client:
    # Initializes a S3 utils tool. 
    def __init__(self):
        load_dotenv()
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.getenv('AWS_DEFAULT_REGION')
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        
        self.s3_session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )
        self.s3 = self.s3_session.resource('s3')

    # Converts an image url to an np.array for storage. 
    def download_image_as_array(self, url: str):
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        image_array = np.array(image)
        return image_array

    # Stores an entry into our S3 database. 
    def put_object(self, image_array: np.ndarray, flow_index: int, month: str, flowerName: str):
        object_key = f"{flow_index:04}_{month}_{flowerName}.json"
    
        flower_data = {
            'index': flow_index,
            'month': month,
            'flowername': flowerName,
            'image': image_array.tolist()
        }
        
        data_str = json.dumps(flower_data)
        
        response = self.s3.Object(self.bucket_name, object_key).put(Body=data_str)
        return response