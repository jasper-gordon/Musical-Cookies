from Population import Population
from Recipe import Recipe
from Ingredient import Ingredient
from Population import lyric_gatherer
from Population import ingredient_matcher

#mypop = Population(1, "practice_input/*.txt", .3)

knowledge_list = []
artist = "Weird Al"
lyrics = lyric_gatherer(8, artist)
song_ingredients = ingredient_matcher(lyrics)

#ADD USER INPUT REPEATED REQUESTS FOR BAD INPUT

for item in song_ingredients:
    food = Ingredient(item, 1, "oz")
    knowledge_list.append(food)


mypop = Population(3, "https://www.tasteofhome.com/collection/the-best-cookie-recipes/", .3, knowledge_list, artist)
best_recipe = mypop.generate()
print (best_recipe)
print ("And here is its score: " + str(best_recipe.evaluation))




#print(mypop)

#myingredient = [Ingredient("flour", 2.5)]
#print (myingredient)

#myrecipe = Recipe("bread", myingredient)
#print (myrecipe)