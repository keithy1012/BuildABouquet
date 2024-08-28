import boto3
from boto3.dynamodb.conditions import Key, Attr
from dotenv import load_dotenv
import os

# Stores flower names, image urls, and month in AWS DynamoDB.
class DynamoDB:
    # Initializes a DynamoDB utils tool.
    def __init__(self):
        load_dotenv()
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.getenv('AWS_DEFAULT_REGION')
        self.partition_key = os.getenv('PARTITION_KEY')
        
        self.dynamodb_session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )
        self.dynamodb = self.dynamodb_session.resource('dynamodb')
        self.table = self.dynamodb.Table('flower-bouquet')

    # Adds an index to the database. 
    def put_item(self, flow_index: int, month: str, flowerName: str, image_url: str):
        item = {
            self.partition_key: flow_index,
            'month': month,
            'flowername': flowerName,
            'image_url': image_url   
        }
        response = self.table.put_item(Item=item)
        return response

    # Returns all flowers that fill in a certain month. 
    def get_items_by_month(self, month: str):
        try:
            response = self.table.query(
                IndexName='month-index',
                KeyConditionExpression=Key('month').eq(month)
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"Error retrieving items by month: {e}")
            return None