import nltk
from nltk import word_tokenize, pos_tag
import json

# An NLP utils class to process user inputted data. 
class InputProcessor:
    # Initilizes our InputProcessor tool.
    def __init__(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

    # Takes a user input and performs standard NLP processes by parts of speech. 
    def process_input(self, user_input):
        tokens = word_tokenize(user_input)
        tagged_pos = pos_tag(tokens)
        season = None
        number_of_flowers = None
        adjectives = []

        seasons = {'spring', 'summer', 'autumn', 'fall', 'winter'}

        for word, tag in tagged_pos:
            if tag == 'CD':
                number_of_flowers = int(word)

            elif tag == 'JJ':
                adjectives.append(word)
            
            elif word.lower() in seasons:
                season = word.lower()

        #print(f"Season: {season}")
        #print(f"Number of flowers: {number_of_flowers}")
        #print(f"Adjectives describing flowers: {', '.join(adjectives)}")
        output = {
            "season": season,
            "number_of_flowers": number_of_flowers,
            "adjectives": adjectives
        }
        return output
