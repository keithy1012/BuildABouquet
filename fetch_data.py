import requests
from bs4 import BeautifulSoup
import csv 
from db.dynamodb import DynamoDB
from db.s3 import S3Client

dynamo = DynamoDB()
s3 = S3Client()

# URL of the Flower Database
base_url = "https://www.flower-db.com/en/search"
csv_file = "flowers.csv"

# Function to get flowers by month
def get_flowers_by_month(month, page):
    url = f"{base_url}/seasons?q={month}&page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    flower_section = soup.find("div", class_="row row-cols-2 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-2 mt-3 mt-md-0")
    flowers = []
    for flower in flower_section.find_all("div", class_="col"):
        name = flower.find("h2").text.strip()
        #print("Flower Name: ", name)
        img_url = base_url + flower.find("img", class_="card-img-top")["src"]
        second_https_pos = img_url.find('https:', img_url.find('https:') + 1)

        # Extract the substring from the second 'https:'
        img_url = img_url[second_https_pos:]

        #print("Flower Picture: " , img_url)
        flowers.append({"name": name, "img_url": img_url})
    
    return flowers

months = ["january", "february", "march", "april", "may", "june", 
          "july", "august", "september", "october", "november", "december"]
flowers = {}


with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    #writer.writerow(["Month", "Flower Name", "Image URL"])
    flow_index = 0
    month_index = 1
    for month in months:
        print(month)
        flowers_list = []
        page = 1
        new_page = True
        while new_page:
            flowers = get_flowers_by_month(month, page)
            if flowers[0]['name'] in flowers_list:
                print("Max Pages for ", month, ": ", page)
                page = 1
                new_page = False
                continue
            for flower in flowers:
                    #writer.writerow([month.capitalize(), flower['name'], flower['img_url']])
                    flowers_list.append(flower["name"])
                    if flow_index > 4188:
                        response = dynamo.put_item(flow_index, month.capitalize(), flower['name'], flower['img_url'])
                        image_arr = s3.download_image_as_array(flower['img_url'])
                        s3.put_object(image_arr, flow_index, month.capitalize(), flower['name'], )
                    print(flow_index, flower["name"])
                    flow_index+=1

            page += 1
        month_index += 1

print(flow_index)
