
class Ingredient: 

    def __init__(self), name, amount, unit):
        self.name = name
        self.amount = amount
        self.unit = unit

    #Returns string representation of this Ingredient
    def __str__(self):
        output = str(self.amount) + self.unit + self.name
        return output

    def __repr__(self):
        return "Ingredient('{0}', {1}, '{2}')".format(self.name, self.amount, self.unit)

    def get_amount(self):
        return self.amount