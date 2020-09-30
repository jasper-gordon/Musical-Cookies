
import glob
from Recipe import Recipe
from Ingredient import Ingredient
import random
import sys, getopt


class Population:

    def __init__(self, generations, mutate_prob):
        self.population = []
        self.knowledge_base = []
        self.generations = generations
        self.mutate_prob = mutate_prob


    def generate(self):
        best_cookie = self.population[0]
        for i in range(0, self.generations):
            self.select()
            self.crossover():
            self.mutate():

            for cookie in self.population:
                if best_cookie.evaluate() <= cookie.evaluate():
                    best_cookie = cookie

    def select():

        recipes = self.population
        sample_list = []
        breeding_pool = []

        ranked_recipes = sorted(recipes)
        rank = 1
        for recipe in ranked_recipes:
            sample_list = sample_list + rank*[recipe]
            rank += 1

        for i in range(0, len(self.population)):
            random.shuffle(sampling_list) #Randomly shuffles list
            breeding_pool.append(sampling_list[0])

        self.population = breeding_pool


    def crossover(self):

        #Every recipe needs flour, sugar, and an egg

        #basic_ingredients = {'flour': , 'sugar': , 'butter': }


    def mutate(self):
        for i in range(0, len(self.population)):
            self.population[i].mutate(self.mutate_prob, self.knowledge_base)
