"""Names: Vincent Dong, Tenzin Choezin, Jasper Gordon
Course: CSCI 3725
Assignment: PQ2
Date: 10/15/2020
Description: This file handles the Recipe class. The class constructor takes a name, and list of ingredient objects
    as arguments. The purpose of the class is to build Recipe objects which can be used and manipulated by
    the Population class to build Recipe objects with new combinations of Ingredients and amounts."""
from Ingredient import Ingredient
import random
import lyricsgenius
import numpy as np
import FlavorPairingQuickstart as fpq

#Setting up and using the lyric genius API from: https://docs.genius.com/
#Using Flavor Simularity & Food Category Datasets
WORD_EMBED_VALS = np.load('ingred_word_emb.npy', allow_pickle=True).item()
INGRED_CATEGORIES = np.load('ingred_categories.npy', allow_pickle=True).item()
INGREDIENT_LIST = sorted(WORD_EMBED_VALS.keys())
CONSTANT_MIN_PIVOT = 6


class Recipe:


    def __init__(self, name, ingredient_list):
        """
        An initiliazing method for any new object of the Recipe class that takes a string name and a list of Ingredient
            objects as arguments.
        """
        self.name = name
        self.ingredient_list = ingredient_list
        self.evaluation = self.evaluate()

    def __str__(self):
        """
        Returns a string representation of this Recipe.
        """
        output = self.name + "\n"
        for i in self.ingredient_list:
            output += str(i) + "\n"
        return output[:-1]

    def __repr__(self):
        """
        Returns an object of the same value.
        """
        return "Recipe('{0}', '{1}')".format(self.name, self.ingredient_list)

    def __lt__(self, other):
        """
        A comparison method to the current Recipe object to another using their respective fitness amounts.
        Returns a boolean
        """
        return self.evaluation < other.evaluation

    def evaluate(self):
        """
        A method to determine the value of the recipe object. A recipe score is based off
            the sum of the ingredient paring scores of its ingredients. Method calculates the
            scores of every pairing of ingredients within the recipe where both ingredients
            are in the known ingreedient list so that they are in the pairing database.
            Returns the overall score of the Recipe. 
        """
        score = 0.0
        for ingredient1 in self.ingredient_list:
            #The ingredient name
            n1 = ""
            if ingredient1.name in INGREDIENT_LIST:
                n1 = ingredient1.name
            #Case if part of name is in known ingredient list exp: 'vanilla' where 'vanilla extract'
            #is in the ingredient list
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
                #Calculating the score of the pairing between the two distinct ingredients
                score += fpq.similarity(n1, n2)
        return score

    def mutate(self, mutate_prob, knowledge_base, artist_name):
        """
        Method to mutate a the Recipe object in a variety ways. Takes a mutation probability which is a 
            float value between 0 and 1 to determine mutation, a knowledge base which is a list of known 
            Ingredient objects, an artist a name which is a string. 
            """
        basic_name = ""
        name_strings =  [artist_name + "'s Famous", basic_name, "Cookies"]
        r = random.uniform(0,1)
        #Choosing whether to mutate or not
        if r > mutate_prob:
            pass
        #Choosing which mutation to execute
        else:
            mutation_type_prob = random.uniform(0,1)
            if mutation_type_prob <= .9:
                self.song_ingredient_add(knowledge_base, name_strings)
            #Delete ingredient from recipe
            else:
                self.ingredient_list[(random.randint(CONSTANT_MIN_PIVOT,len(self.ingredient_list) - 1))].amount = 0

    def song_ingredient_add(self, knowledge_base, name_strings):
        """Executes a mutation where it adds an Ingredient object to the Recipe from the
                song ingredient list if the ingredient is not already in the Recipe.
                If it is, then instead it adds an ingredient that pairs with the
                chosen song ingredient.
                Args: the knowledge base which is a list of known Ingredients, and
                the name strings which holds the name of the Recipe. """
        random_value = random.randint(0, len(knowledge_base) - 1)
        song_ingredient = knowledge_base[random_value]
        #If the randomly chosen song Ingredient is already in the Recipe
        if song_ingredient in self.ingredient_list:
            pairing_list = fpq.request_pairing(song_ingredient.name, .1)
            random_value2 = random.randint(0, len(pairing_list) - 1)
            pairing_ingredient = Ingredient(pairing_list[random_value2], 1, "oz")
            self.ingredient_list.append(pairing_ingredient)
        #If the randomly chosen song Ingredient is NOT already in the Recipe
        else:
            self.ingredient_list.append(song_ingredient)
            name_strings[1] = song_ingredient.name
            self.name = " ".join(name_strings)
