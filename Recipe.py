
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