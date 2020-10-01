
from Ingredient import Ingredient
import random

class Recipe:

    """"An initiliazing method for any new object of the Recipe class that takes a string name and a list of Ingredient
            objects as arguments."""
    def __init__(self, name, ingredient_list):
        self.name = name
        self.ingredient_list = ingredient_list


    """Returns a string representation of this Recipe."""
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
        return self.evaluate() < other.evalueate()

    def evaluate(self):
        return len(self.ingredient_list)
