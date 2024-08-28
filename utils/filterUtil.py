
from db.dynamodb import DynamoDB
from db.s3 import S3Client
from .flowerUtil import FlowerUtil
from .model import HSVAdjectiveNN

SEASONS = {
    'spring' : ["March", "April", "May"],
    'summer' : ["June","July", "August"],
    'fall' : ["September", "October", "November"],
    'winter' : ["January", "February","December"]
}

# Utility methods that filter out flowers
class FilterUtils:
    # Initializes a FilterUtils tool. 
    def __init__(self):
        #self.s3 = S3Client()
        self.db = DynamoDB()
        self.flowerUtil = FlowerUtil()
        self.hsvPredictor = HSVAdjectiveNN()

    # Filters flowers based on the user-inputted season. 
    def filterFlowersBySeason(self, season: str):
        months = SEASONS.get(season, [])
        all_flowers = []
        
        for month in months:
            items = self.db.get_items_by_month(month)
            if items:
                for flower in items:
                    all_flowers.append(flower)
        print("Total Flowers: ", len(all_flowers))
        return all_flowers

    # Filters flowers based on the user-inputted adjectives. 
    def filterFlowersByAdj(self, flowers:list, adj:list):
        filtered_flowers = []
        for flower in flowers:
            image_url = flower['image_url']
            top_colors, hsv_values = self.flowerUtil.get_top_colors(image_url)
            flower_image_adj = self.hsvPredictor.predict_weighted(top_colors)
            print(image_url, flower_image_adj)
            '''
            flower_image_adj = self.hsvPredictor.predict(hsv_values[0])
            print(image_url,flower_image_adj)

            Using spacy to compare similarity of user adj and flower_image_adj
            if probability > 0.7:
                filtered_flowers.append(flower)
            '''

        return filtered_flowers
