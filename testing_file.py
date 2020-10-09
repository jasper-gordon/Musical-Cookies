from Population import Population
from Recipe import Recipe
from Ingredient import Ingredient
from Population import lyric_gatherer
from Population import ingredient_matcher

#mypop = Population(1, "practice_input/*.txt", .3)

knowledge_list = []
artist = "Jimmy Buffett"
lyrics = lyric_gatherer(4, artist)
song_ingredients = ingredient_matcher(lyrics)

#ADD USER INPUT REPEATED REQUESTS FOR BAD INPUT

for item in song_ingredients:
    food = Ingredient(item, 1, "oz")
    knowledge_list.append(food)


mypop = Population(1, "https://www.tasteofhome.com/collection/the-best-cookie-recipes/", .3, knowledge_list)
print (mypop.generate())





#print(mypop)

#myingredient = [Ingredient("flour", 2.5)]
#print (myingredient)

#myrecipe = Recipe("bread", myingredient)
#print (myrecipe)