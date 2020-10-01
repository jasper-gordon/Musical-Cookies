
import glob
from Recipe import Recipe
from Ingredient import Ingredient
import random
import sys
import getopt

CONSTANT_MIN_PIVOT = 3  # crossover pivot will always be > 3,
# first 3 indexes in a cookie recipe's ingredient list will be a flour, a sugar,
# and a fat, which is needed to be present in every cookie recipe


class Population:

    def __init__(self, generations, mutate_prob):
        self.population = []
        self.knowledge_base = []
        self.generations = generations
        self.mutate_prob = mutate_prob

        current_file = open(filename, "r")
        current_recipe = []
        for line in current_file:
            line = line.strip()
            words = line.split(" ", 2)
            # Creating new Ingredient object with name, quantity, and unit
            new_ingredient = Ingredient(words[2], float(words[0], words[1]))
            recipe.append(new_ingredient)
        new_recipe = Recipe(filename[6:-4], current_recipe)
        self.population.append(new_recipe)

    def generate(self):
        best_cookie = self.population[0]
        for i in range(0, self.generations):
            self.select()
            self.crossover():
            self.mutate():

            for cookie in self.population:
                if best_cookie.evaluate() <= cookie.evaluate():
                    best_cookie = cookie

        return self.population

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
            random.shuffle(sampling_list)  # Randomly shuffles list
            breeding_pool.append(sampling_list[0])

        self.population = breeding_pool

    def crossover(self):
        parents = self.population
        random.shuffle(parents)
        next_generation = []

        def one_point_crossover(parent1, parent2):
            pivot1 = random.randint(CONSTANT_MIN_PIVOT), len(parent1.ingredient_list) - 1)
            pivot2=random.randint(CONSTANT_MIN_PIVOT, len(
                parent2.ingredient_list) - 1)

            parent1_sublist1=parent1.ingredient_list[:pivot1]
            parent1_sublist2=parent1.ingredient_list[pivot1:]
            parent2_sublist1=parent2.ingredient_list[:pivot2]
            parent2_sublist2=parent2.ingredient_list[pivot2:]

            new_recipe1_list=parent1_sublist1 + parent2_sublist2
            new_recipe2_list=parent2_sublist1 + parent1_sublist2

            # Helper method, gets rid of duplicate ingredients in ingredient list
            def clean(recipe):
                ingredient_dict={}
                unique_ingredients=[]
                for ingredient in recipe:
                    if ingredient.name in ingredient_dict:
                        ingredient_dict[ingredient.name] += ingredient.amount
                    else:
                        ingredient_dict[ingredient.name]=ingredient.amount
                        unique_ingredients.append(ingredient)
                for ingredient in unique_ingredients:
                    ingredient.amount=ingredient_dict[ingredient.name]
                return unique_ingredients

            cleaned_recipe1=clean(new_recipe1_list)
            cleaned_recipe2=clean(new_recipe2_list)

            return cleaned_recipe1, cleaned_recipe2

        # Go through shuffled breeding_pool and picks pairs
        for i in range(0, len(self.population), 2):
            child1_list, child2_list=one_point_crossover(
                parents[i], parents[i+1])
            parent1_name=parents[i].name.split()
            parent2_name=parents[i+1].name.split()
            pivot1=random.randint(1, len(parent1.ingredient_list) - 1)
            pivot2=random.randint(1, len(parent2.ingredient_list) - 1)

            parent1_sublist1=parent1_name[:pivot1]
            parent1_sublist2=parent1_name[pivot1:]
            parent2_sublist1=parent1_name[:pivot2]
            parent2_sublist2=parent1_name[pivot2:]

            child1_name=" ".join(parent1_sublist1 + parent2_sublist2)
            child2_name=" ".join(parent2_sublist1 + parent1_sublist2)

            child1=Recipe(child1_name, child1_list)
            child2=Recipe(child2_name, child2_list)
            next_generation.append(child1)
            next_generation.append(child2)

        self.population=next_generation
        # Every recipe needs flour, sugar, and an egg
        # basic_ingredients = {'flour': , 'sugar': , 'butter': }


    def mutate(self):
        for i in range(0, len(self.population)):
            self.population[i].mutate(self.mutate_prob, self.knowledge_base)
