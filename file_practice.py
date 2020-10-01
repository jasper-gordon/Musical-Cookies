
print("hello")

'''
for filename in glob.glob(filepath_folder):
            # List of tuples to hold ingredients and quantities
            current_recipe = []
            current_file = open(filename, "r")
            for line in current_file:
                line = line.strip()
                words = line.split("[0-9A-Za-z]+\s[0-9A-Za-z]+\s.*")
                #Creating new Ingredient object with name and quantity
                new_ingredient = Ingredient(words[1], float(words[0]))
                current_recipe.append(new_ingredient)
                if words[1] not in self.total_ingredients:
                    self.total_ingredients.append(words[1])

            new_recipe = Recipe(filename[6:-4], current_recipe)
            self.population.append(new_recipe)
            '''

print ("hello")