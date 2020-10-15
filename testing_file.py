from Population import Population
from Recipe import Recipe
from Ingredient import Ingredient
from Population import lyric_gatherer
from Population import ingredient_matcher

#mypop = Population(1, "practice_input/*.txt", .3)
'''
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
'''

"""
Main method that runs our Genetic Algorithm system
"""
def main():
    print ("\n Welecome to the Cookie Monster brought to you by the team at Too Many Cooks Kitchen \n Our cookie generator takes in any known Musical Artist, scours their songs for any culinary inspiration, \n and then adapts common cookie recipies to have a little taste of fame in them.")
    print ("For each of the following prompts, please input your data and then press 'Return' \n")
    print ("Please input your desired number of generations: ")
    generations_input = int(input())
    print ("Please input a musical artist. Many artists do not reference food in their songs so don't be detterd if you are unlucky, just keep trying!")
    artist_name = str(input())
    print ("Please input your desired recipe mutation rate. This is any value between 0 and 1 and it effects the odds that your recipe has that extra taste of")
    print(" your favorite star. The recommened range for input is between .5 and .7 but try feel free to adjust and try multiple times!")
    mutation_intput = float(input())
    knowledge_list = []
    lyrics = lyric_gatherer(8, artist_name)
    song_ingredients = ingredient_matcher(lyrics)
    for item in song_ingredients:
        food = Ingredient(item, 1, "oz")
        knowledge_list.append(food)
    mypop = Population(generations_input, "https://www.tasteofhome.com/collection/the-best-cookie-recipes/", mutation_intput, knowledge_list, artist_name)
    best_recipe = mypop.generate()
    print (best_recipe)
    print ("And here is its score: " + str(best_recipe.evaluation))

if __name__ == "__main__":
    main()


#print(mypop)

#myingredient = [Ingredient("flour", 2.5)]
#print (myingredient)

#myrecipe = Recipe("bread", myingredient)
#print (myrecipe)