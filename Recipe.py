
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
        pass

    #Gathers the lyrics for given int value of songs of the given artist
    #Returns the group of lyrics as a list of strings
    def lyric_gatherer(self, song_limit):
        lyric_list = []
        songs = genius.search_artist(self.artist_name, max_songs = song_limit, sort = "popularity" ).songs
        for song in songs:
            unique_lyrics = []
            unfiltered_lyrics = song.lyrics.split()
            #Only taking unique words from the lyrics to avoid repeats
            for line in unfiltered_lyrics:
                if line not in unique_lyrics:
                    #Adjusts case to lower to make sure it is comparable to ingredient_list
                    unique_lyrics.append(line.lower())
            #Adding all new unique lyrics to the full list of the artist's lyrics
            lyric_list.extend(unique_lyrics)
        return lyric_list

    #Method to check if any real ingredients in a song list
    #Returns a list of ingredients (strings)
    def ingredient_matcher(self, lyrics):
        real_ingredients = []
        for word in lyrics:
            if word in INGREDIENT_LIST:
                real_ingredients.append(word)
        return real_ingredients
