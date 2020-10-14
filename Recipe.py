
from Ingredient import Ingredient
import random
import lyricsgenius
import numpy as np
import FlavorPairingQuickstart as fpq

genius = lyricsgenius.Genius("dEVN1E_5EEdG87GGOurKdFhPFkx-k-yTztAOSNJRkutxNoJmX4pI_38cBNPCUDTY")
#genius.verbose = False
genius.remove_section_headers = True
WORD_EMBED_VALS = np.load('ingred_word_emb.npy', allow_pickle=True).item()
INGRED_CATEGORIES = np.load('ingred_categories.npy', allow_pickle=True).item()
INGREDIENT_LIST = sorted(WORD_EMBED_VALS.keys())

class Recipe:

    """
    An initiliazing method for any new object of the Recipe class that takes a string name and a list of Ingredient
            objects as arguments.
    """

    def __init__(self, name, ingredient_list):
        self.name = name
        self.ingredient_list = ingredient_list
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
        score = 0.0
        for ingredient1 in self.ingredient_list:
            n1 = ""
            if ingredient1.name in INGREDIENT_LIST:
                n1 = ingredient1.name
            else:
                ing1_parts = ingredient1.name.split(" ")
                for part in ing1_parts:
                    if part in INGREDIENT_LIST:
                        n1 = part
            if not n1:
                continue

            for ingredient2 in self.ingredient_list:
                n2 = ""
                if ingredient1.name == ingredient2.name:
                    continue
                elif ingredient2.name in INGREDIENT_LIST:
                    n2 = ingredient2.name
                else:
                    ing2_parts = ingredient2.name.split(" ")
                    for part in ing2_parts:
                        if part in INGREDIENT_LIST:
                            n2 = part
                if not n2:
                    continue

                score += fpq.similarity(n1, n2)

        return score

    def mutate(self, mutate_prob, knowledge_base, artist_name):
        #Add ingredient from song list, if ingredeint already there then add a pairing
        basic_name = ""
        name_strings =  [artist_name + "'s Famous", basic_name, "Cookies"]
        r = random.uniform(0,1)
        if r > mutate_prob:
            pass
        if mutate_prob <= .4:
            random_value = random.randint(0, len(knowledge_base) - 1)
            song_ingredient = knowledge_base[random_value]
            if song_ingredient in self.ingredient_list:
                pairing_list = fpq.request_pairing(song_ingredient.name, .1)

                #NEED TO MAKE METHOD TO GENERATE BIASED LIST

                random_value2 = random.randint(0, len(pairing_list) - 1)
                pairing_ingredient = Ingredient(pairing_list[random_value2], 1, "oz")
                self.ingredient_list.append(pairing_ingredient)
            else:
                self.ingredient_list.append(song_ingredient)
                name_strings[1] = song_ingredient.name
                self.name = " ".join(name_strings)
         #Swap ingredient with ingredient from song list
        elif mutate_prob <= .8:
            pass
        #Delete ingredient from recipe
        else:
            self.ingredient_list.remove(random.randint(2,len(self.ingredient_list) - 1))
        
