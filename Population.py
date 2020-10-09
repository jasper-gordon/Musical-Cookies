
import glob
from Recipe import Recipe
from Ingredient import Ingredient
import random
import sys
import getopt
from Webscraping import *
from fractions import Fraction
import numpy as np
import lyricsgenius
genius = lyricsgenius.Genius("dEVN1E_5EEdG87GGOurKdFhPFkx-k-yTztAOSNJRkutxNoJmX4pI_38cBNPCUDTY")
#genius.verbose = False
genius.remove_section_headers = True
WORD_EMBED_VALS = np.load('ingred_word_emb.npy', allow_pickle=True).item()
INGRED_CATEGORIES = np.load('ingred_categories.npy', allow_pickle=True).item()
INGREDIENT_LIST = sorted(WORD_EMBED_VALS.keys())
CONSTANT_MIN_PIVOT = 5  # crossover pivot will always be > 3,
# first 3 indexes in a cookie recipe's ingredient list will be a flour, a sugar,
# and a fat, which is needed to be present in every cookie recipe


class Population:

    def __init__(self, generations, filepath_folder, mutate_prob, knowledge_base, artist_name):
        self.population = []
        self.knowledge_base = knowledge_base
        self.generations = generations
        self.mutate_prob = mutate_prob
        self.recipe_counter = 1
        self.artist_name = artist_name

        #for filename in glob.glob(filepath_folder):
        #current_file = open(filename, "r")
        # calling web scrpaing method from the Webscraping file, giving it URL
        print("Me no resist cookies.")
        cookie_dict = web_scraper(filepath_folder)
        for cookie_name in cookie_dict:
            current_recipe = []
            for element in cookie_dict[cookie_name]:
                #line = line.strip()
                words = element.split(" ", 2)

                #PROBLEM AREA - Trying to check if - is in string and if so remove that portion of the stirng (i.e. 2-1/2 becomes 2)
                if "-" in words[0]:

                    words[0] = words[0].split("-")[0]

                # Dealing with lines with no units (exp "2 eggs")
                if len(words) == 2:
                    words.append (" ")
                 # Creating new Ingredient object with name, quantity, and unit

                is_num = False

                if words[0][0].isdigit():
                    is_num = True

                if is_num:
                    new_ingredient = Ingredient(words[2], float(Fraction(words[0])), words[1])
                    current_recipe.append(new_ingredient)
            # Setting flour and sugar to the front of the list
            flour = Ingredient('flour', 0, "cup")
            sugar = Ingredient('sugar', 0, "cup")
            butter = Ingredient('butter', 0, "cup")
            egg = Ingredient('egg', 0, "")
            salt = Ingredient('salt', 0, "teaspoons")
            flour_index = 0
            sugar_index = 0
            butter_index = 0
            egg_index = 0
            salt_index = 0

            for ingredient in current_recipe:
                if 'flour' in ingredient.name:
                    flour = ingredient
                    break
                flour_index += 1

            #if(len(current_recipe) == 4 or len(current_recipe) == 5):
            #    continue

            if flour_index < len(current_recipe):
                current_recipe.pop(flour_index)

            for ingredient in current_recipe:
                if 'sugar' in ingredient.name:
                    sugar = ingredient
                    break
                sugar_index += 1

            if sugar_index < len(current_recipe):
                current_recipe.pop(sugar_index)

            for ingredient in current_recipe:
                if 'butter' in ingredient.name:
                    butter = ingredient
                    break
                butter_index += 1

            if butter_index < len(current_recipe):
                current_recipe.pop(butter_index)

            for ingredient in current_recipe:
                if 'egg' in ingredient.name:
                    egg = ingredient
                    break
                egg_index += 1

            if egg_index < len(current_recipe):
                current_recipe.pop(egg_index)

            for ingredient in current_recipe:
                if 'salt' in ingredient.name:
                    salt = ingredient
                    break
                salt_index += 1

            if salt_index < len(current_recipe):
                current_recipe.pop(salt_index)


            current_recipe.insert(0,sugar)
            current_recipe.insert(0,flour)
            current_recipe.insert(0,butter)
            current_recipe.insert(0,egg)
            current_recipe.insert(0,salt)

            #new_recipe = Recipe(filename[15:-4], current_recipe)
            new_recipe = Recipe(cookie_name, current_recipe)
            self.recipe_counter += 1
            self.population.append(new_recipe)

    """
    Returns string representation of Population.
    """
    def __str__(self):
        #Returns a string representation of this Population
        output = ""
        for i in self.population:
            output += str(i)
        return output

    """
    Lets us make an object of the same value.
    """
    def __repr__(self):
        return "Population('{0}')".format(self.population)

    def generate(self):
        best_cookie = self.population[0]
        for i in range(0, self.generations):
            self.select()
            self.crossover()
            self.mutate()

            for cookie in self.population:
                if best_cookie.evaluation <= cookie.evaluation:
                    best_cookie = cookie
        trash_list = []
        for item in best_cookie.ingredient_list:
            if item.amount == 0:
                trash_list.append(item)
        for junk in trash_list:
            best_cookie.ingredient_list.remove(junk)
        return best_cookie

    def select(self):

        recipes = self.population
        sample_list = []
        breeding_pool = []

        ranked_recipes = sorted(recipes)
        rank = 1
        for recipe in ranked_recipes:
            sample_list = sample_list + rank*[recipe]
            rank += 1

        for i in range(0, len(self.population)):
            random.shuffle(sample_list)  # Randomly shuffles list
            breeding_pool.append(sample_list[0])

        self.population = breeding_pool

    def crossover(self):
        parents = self.population
        random.shuffle(parents)
        next_generation = []

        def one_point_crossover(parent1, parent2):
            pivot1 = random.randint((CONSTANT_MIN_PIVOT), len(parent1.ingredient_list) - 1)
            pivot2 = random.randint(CONSTANT_MIN_PIVOT, len(
                parent2.ingredient_list) - 1)

            parent1_sublist1 = parent1.ingredient_list[:pivot1]
            parent1_sublist2 = parent1.ingredient_list[pivot1:]
            parent2_sublist1 = parent2.ingredient_list[:pivot2]
            parent2_sublist2 = parent2.ingredient_list[pivot2:]

            new_recipe1_list = parent1_sublist1 + parent2_sublist2
            new_recipe2_list = parent2_sublist1 + parent1_sublist2

            # Helper method, gets rid of duplicate ingredients in ingredient list
            def clean(recipe):
                ingredient_dict = {}
                unique_ingredients = []
                for ingredient in recipe:
                    if ingredient.name in ingredient_dict:
                        ingredient_dict[ingredient.name] += ingredient.amount
                    else:
                        ingredient_dict[ingredient.name] = ingredient.amount
                        unique_ingredients.append(ingredient)
                for ingredient in unique_ingredients:
                    ingredient.amount = ingredient_dict[ingredient.name]
                return unique_ingredients

            cleaned_recipe1 = clean(new_recipe1_list)
            cleaned_recipe2 = clean(new_recipe2_list)

            return cleaned_recipe1, cleaned_recipe2

        # Go through shuffled breeding_pool and picks pairs
        for i in range(0, len(self.population), 2):
            child1_list, child2_list = one_point_crossover(parents[i], parents[i+1])


            child1 = Recipe(parents[i].name, child1_list)
            child2 = Recipe(parents[i + 1].name, child2_list)
            next_generation.append(child1)
            next_generation.append(child2)
            self.recipe_counter += 1
        self.population = next_generation
        # Every recipe needs flour, sugar, and an egg
        # basic_ingredients = {'flour': , 'sugar': , 'butter': }


    def mutate(self):
        for i in range(0, len(self.population)):
            self.population[i].mutate(self.mutate_prob, self.knowledge_base, self.artist_name)



#for i in INGREDIENT_LIST:
    #print (i)

#Method to check if any real ingredients in a song list
#Returns a list of ingredients (strings)
def ingredient_matcher(lyrics):
    real_ingredients = []
    for word in lyrics:
        if word in INGREDIENT_LIST:
            real_ingredients.append(word)
    return real_ingredients

#Gathers the lyrics for given int value of songs of the given artist
#Returns the group of lyrics as a list of strings
def lyric_gatherer(song_limit, artist_name):
    lyric_list = []
    try:
        songs = genius.search_artist(artist_name, max_songs = song_limit, sort = "popularity" ).songs
    except:
        print("This artist input is invalid")
        return lyric_list
    else:
        print("made it this far")
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

def main():
    knowledge_list = []
    artist = "Jimmy Buffett"
    lyrics = lyric_gatherer(4, artist)
    song_ingredients = ingredient_matcher(lyrics)

    #ADD USER INPUT REPEATED REQUESTS FOR BAD INPUT

    for item in song_ingredients:
        food = Ingredient(item, 1, "oz")
        knowledge_list.append(food)
