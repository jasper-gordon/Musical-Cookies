
from Ingredient import Ingredient
import random
import lyricsgenius
import numpy as np

genius = lyricsgenius.Genius("dEVN1E_5EEdG87GGOurKdFhPFkx-k-yTztAOSNJRkutxNoJmX4pI_38cBNPCUDTY")
#genius.verbose = False
genius.remove_section_headers = True
WORD_EMBED_VALS = np.load('ingred_word_emb.npy', allow_pickle=True).item()
INGRED_CATEGORIES = np.load('ingred_categories.npy', allow_pickle=True).item()
INGREDIENT_LIST = sorted(WORD_EMBED_VALS.keys())

class Recipe:

    """
    An initiliazing method for any new object of the Recipe class that takes a string name, a list of Ingredient
            objects, and a string Artist name as arguments.
    """

    def __init__(self, name, ingredient_list, artist_name):
        self.name = name
        self.ingredient_list = ingredient_list
        self.artist_name = artist_name
        self.evaluation = self.evaluate()

    """
    #Returns a string representation of this Recipe.
    """
    def __str__(self):
        output = self.name + "\n"
        for i in self.ingredient_list:
            output += str(i) + "\n"
        return output[:-1]

    """
    A comparison method to the current Recipe object to another using their respective fitness amounts.
    Returns a boolean
    """
    def __lt__(self, other):
        return self.evaluation < other.evaluation

    def evaluate(self):
        for ingredient1 in ingredient_list:
            ing1_parts = ingredient1.name.split(" ")
            for part in ing1_parts:
                if part in INGREDIENT_LIST:
                    return

            if ingredient1.name not in INGREDIENT_LIST:
                continue
            for ingredient2 in ingredient_list:
                if ingredient2 not in INGREDIENT_LIST:
                    continue
                elif ingredient1.name == ingredient2.name:
                    continue
                elif ingredient.name in INGREDIENT_LIST:

        return len(self.ingredient_list)

    def mutate(self, mutate_prob, knowledge_base):
        #Add ingredient from song list, if ingredeint already there then add a pairing
        if mutate_prob <= .4:
            pass
        #Swap ingredient with ingredient from song list
        elif mutate_prob <= .8:
            pass
        #Delete ingredient from recipe
        else:
            self.ingredient_list.remove(random.randint(2,len(self.ingredient_list))


