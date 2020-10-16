"""
Names: Vincent Dong, Tenzin Choezin, Jasper Gordon
Course: CSCI 3725
Assignment: PQ2
Date: 10/14/2020
Description: This file handles the Population class. The class constructor takes
    in the number of generations, recipes_url, the mutation_prob, a knowledge_base,
    and an artist_name as arguements. The main purpose of the class is it runs
    the Genetic Algorithm process on the population, which is a list of Recipe
    objects. The Population.generate() does the GA process, and returns the best
    cookie seen.
"""

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
genius.remove_section_headers = True
WORD_EMBED_VALS = np.load('ingred_word_emb.npy', allow_pickle=True).item()
INGRED_CATEGORIES = np.load('ingred_categories.npy', allow_pickle=True).item()
INGREDIENT_LIST = sorted(WORD_EMBED_VALS.keys())
CONSTANT_MIN_PIVOT = 6  # crossover pivot will always be >= 6,
# first 6 indexes in a cookie recipe's ingredient list will be "essential" ingredients:
# sugar, flour, butter, egg, salt, vanilla extract.


class Population:


    def __init__(self, generations, recipes_url, mutate_prob, knowledge_base, artist_name):
        """
        Population constructor, which takes in generations (int), recipes_url
            (str), mutation_prob (float), knowledge_base (list), artist_name (str),
            and creates a Population object.
        """
        self.population = [] #List of Recipe objects, our population
        self.knowledge_base = knowledge_base #List of ingredient objects, from artist's songs
        self.generations = generations #Number of generations to run GA on the population
        self.mutate_prob = mutate_prob #Mutation probability
        self.artist_name = artist_name #The artist's name
        self.full_score_sheet = [] #List that will be populated with all recipe scores

        # calling web scrpaing method from the Webscraping file, giving it URL
        cookie_dict = web_scraper(recipes_url)
        for cookie_name in cookie_dict:
            current_recipe = []
            for element in cookie_dict[cookie_name]:
                #line = line.strip()
                words = element.split(" ", 2)
                #PROBLEM AREA - Trying to check if - is in string and if so remove that portion of the stirng (i.e. 2-1/2 becomes 2)
                if "-" in words[0]:
                    words[0] = words[0].split("-")[0] #Takes the lower bound of the ingredient amount
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

            def essential_ingredient(ingredient_obj, recipe):
                """
                Helper method, removes ingredient_obj from recipe (ingredient_list)
                """
                index = 0
                essential_obj = None
                for ingredient in recipe:
                    if ingredient_obj.name in ingredient.name:
                        essential_obj = ingredient
                        break
                    index += 1

                if index < len(recipe):
                    recipe.pop(index)

                if not essential_obj:
                    return ingredient_obj, recipe
                else:
                    return essential_obj, recipe

            # Essential Ingredient Objects
            flour = Ingredient('flour', 0, "cup")
            sugar = Ingredient('sugar', 0, "cup")
            butter = Ingredient('butter', 0, "cup")
            egg = Ingredient('egg', 0, "")
            salt = Ingredient('salt', 0, "teaspoons")
            vanilla_extract = Ingredient('vanilla extract', 0, "teaspoons")
            flour, current_recipe = essential_ingredient(flour, current_recipe)
            sugar, current_recipe = essential_ingredient(sugar, current_recipe)
            butter, current_recipe = essential_ingredient(butter, current_recipe)
            egg, current_recipe = essential_ingredient(egg, current_recipe)
            salt, current_recipe = essential_ingredient(salt, current_recipe)
            vanilla_extract, current_recipe = essential_ingredient(vanilla_extract, current_recipe)

            # Insert essential ingredients to front of current_recipe
            current_recipe.insert(0,sugar)
            current_recipe.insert(0,flour)
            current_recipe.insert(0,butter)
            current_recipe.insert(0,egg)
            current_recipe.insert(0,salt)
            current_recipe.insert(0,vanilla_extract)
            new_recipe = Recipe(cookie_name, current_recipe)
            self.population.append(new_recipe)

    def __str__(self):
        """
        Returns string representation of Population.
        """
        output = ""
        for i in self.population:
            output += str(i)
        return output

    def __repr__(self):
        """
        Lets us make an object of the same value.
        """
        return "Population('{0}')".format(self.population)

    def generate(self):
        """
        Generates a cookie using the Genetic Algorithm process
        """
        best_cookie = self.population[0] #Initiliazing best_cookie
        for i in range(0, self.generations):
            self.select()
            self.crossover()
            self.mutate()
            generation_score_sheet = [] #List holding scores for all recipe scores in generation
            for cookie in self.population:
                generation_score_sheet.append(cookie.evaluation)
                if best_cookie.evaluation <= cookie.evaluation:
                    best_cookie = cookie
            score_sum = 0
            for score in generation_score_sheet:
                score_sum += score
            average_score = score_sum/len(generation_score_sheet)
            generation_score_sheet.insert(0, average_score)
            self.full_score_sheet.append(generation_score_sheet)

        #Cleaning the best cookie's ingredient list, by removing ingredients with 0 amount
        trash_list = []
        for item in best_cookie.ingredient_list:
            if item.amount == 0:
                trash_list.append(item)
        for junk in trash_list:
            best_cookie.ingredient_list.remove(junk)

        #Naming the best cookie
        ing_name = best_cookie.ingredient_list[-1].name.capitalize()
        name_strings = [self.artist_name + "'s Famous", ing_name, "Cookies"]
        best_cookie.name = " ".join(name_strings)
        return best_cookie

    def select(self):
        """
        Method that selects the breeding pool from current population, using Rank Selection.
        """
        recipes = self.population
        sample_list = []
        breeding_pool = []
        ranked_recipes = sorted(recipes) #Sorted by evaluation score
        rank = 1
        for recipe in ranked_recipes:
            sample_list = sample_list + rank*[recipe]
            rank += 1
        for i in range(0, len(self.population)):
            random.shuffle(sample_list)  # Randomly shuffles list
            breeding_pool.append(sample_list[0])
        self.population = breeding_pool

    def crossover(self):
        """
        Method that performs crossover on the population, which at this stage is the breeding pool.
        """
        parents = self.population
        random.shuffle(parents)
        next_generation = []

        def one_point_crossover(parent1, parent2):
            """
            Helper method that performs crossover on two recipe objects.
            Returns two new ingredient lists
            """
            # Pivot always >= CONSTANT_MIN_PIVOT, which is the number of essential ingredients
            #   at the front of every recipe object's ingredient_list
            pivot1 = random.randint((CONSTANT_MIN_PIVOT), len(parent1.ingredient_list) - 1)
            pivot2 = random.randint(CONSTANT_MIN_PIVOT, len(
                parent2.ingredient_list) - 1)
            parent1_sublist1 = parent1.ingredient_list[:pivot1]
            parent1_sublist2 = parent1.ingredient_list[pivot1:]
            parent2_sublist1 = parent2.ingredient_list[:pivot2]
            parent2_sublist2 = parent2.ingredient_list[pivot2:]
            new_recipe1_list = parent1_sublist1 + parent2_sublist2
            new_recipe2_list = parent2_sublist1 + parent1_sublist2

            def clean(recipe):
                """
                Helper method that gets rid of duplicate ingredients in an ingredient list
                """
                ingredient_dict = {}
                unique_ingredients = []
                for ingredient in recipe:
                    if ingredient.name in ingredient_dict:
                        ingredient_dict[ingredient.name] += (ingredient.amount/self.generations)
                        # Divide by number of generations so we don't overstack a single ingredient amount
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
        self.population = next_generation

    def mutate(self):
        """
        Performs mutation on each Recipe object in the population, calling on
            the Recipe's mutate() function.
        """
        for i in range(0, len(self.population)):
            self.population[i].mutate(self.mutate_prob, self.knowledge_base, self.artist_name)

def ingredient_matcher(lyrics):
    """
    Checks to see if any real ingredients are in the given song list which is an argument.
        Returns a list of Ingredient objects
    """
    real_ingredients = []
    for word in lyrics:
        if word in INGREDIENT_LIST:
            real_ingredients.append(word)
    return real_ingredients

def lyric_gatherer(song_limit, artist_name):
    """
    Gathers the lyrics from the given number (song_limit) of the given artsit's (artist_name) most\
        popular songs. Returns the lyrics from those songs combined in one large list of strings
    """
    lyric_list = []
    try:
        songs = genius.search_artist(artist_name, max_songs = song_limit, sort = "popularity" ).songs
    except:
        print("This artist input is invalid")
        return lyric_list
    else:
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
