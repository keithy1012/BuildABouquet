from utils.userInputProcessor import InputProcessor
from utils.filterUtil import FilterUtils
from flowerCanvas import FlowerCanvas
utils = FilterUtils()
userInputProcessor = InputProcessor()

user_input = "I want 5 bright, saturated, warm flowers for the summer."
request = userInputProcessor.process_input(user_input)
season = request.get('season')
adj = request.get('adjectives')
num_flowers = request.get('number_of_flowers')
print("You want ", num_flowers, " flowers that are: ", adj, " for the season: ", season)

if season:
    filtered_by_season = utils.filterFlowersBySeason(season.lower())
else:
    print("No valid season found in the user input.")


'''
At this point, we have flowers based on the season. 
'''

filtered_flowers = utils.filterFlowersByAdj(filtered_by_season, adj)
#print(len(filtered_flowers))

'''
At this point, we have flowers based on the season and adjectives. 
'''
canvas = FlowerCanvas()
canvas.show_flower_canvas(filtered_flowers)
