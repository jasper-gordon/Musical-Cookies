"""
Names: Vincent Dong, Tenzin Choezin, Jasper Gordon
Course: CSCI 3725
Assignment: PQ2
Date: 10/15/2020
Description: This file handles the Ingredient Class. The purpose of this class is to create and manage Ingredient
    objects that are used to create Recipe objects. An Ingredient object has a string name, a float amount, and then
    a unit which is a string like "cups" or "tsps".
"""
class Ingredient:

    def __init__(self, name, amount, unit):
        """
        Initializes an Ingredient object, taking a string name, float amount, and string unit as arguments.
        """
        self.name = name
        self.amount = amount
        self.unit = unit

    def __str__(self):
        """
        Returns a string representation of an Ingredient Object
        """
        output = str(self.amount) + " " + self.unit + " " +self.name
        return output

    def __repr__(self):
        """
        Returns an object of the same value.
        """
        return "Ingredient('{0}', {1}, '{2}')".format(self.name, self.amount, self.unit)

    def get_amount(self):
        """
        Helper that returns the amount of the Ingredient Object as a float.
        """
        return self.amount

    def __eq__(self, other):
        """
        Helper that compares two Ingredient objects by their names. Returns a boolean.
        """
        return self.name == other.name
