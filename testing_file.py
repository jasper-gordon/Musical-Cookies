"""
Names: Vincent Dong, Tenzin Choezin, Jasper Gordon
Course: CSCI 3725
Assignment: PQ2
Date: 10/15/2020
Description: This file takes in user input and executes the cookie generator program that uses the Population, Recipe, Ingredient, and Webscraping files.
            The purpose of this file is to consolidate all the requests to the user and the run calls in a seperate file maintain organization and control.
"""
from Population import Population
from Recipe import Recipe
from Ingredient import Ingredient
from Population import lyric_gatherer
from Population import ingredient_matcher

#Constant that defines how many of the inputted Artist's most popular songs the LyricsGenius API should look at
NUM_ARTIST_SONGS = 10
#Constant to limit the number of generations the user can request 
GENERATION_LIMIT = 10

def get_generations():
    """Prompts user for the int number of generations they want the program to run. If not given proper input, propmts user again.
        Returns an int.
    """
    generations = ""
    while True:
        try:
            generations = int(input())
            #Ensuring the float is in between 0 and 1
            if generations < 0 or generations > GENERATION_LIMIT:
                print("Invalid input, please give an int value greater than 0.")
                continue
        except ValueError:
            print("Invalid input, please give an int value like '3' or '4'")
            continue
        else:
            break
    return generations

#NEEDS TO MAKE SURE BETWEEN 0 AND 1
def get_mutation_rate():
    """
    Prompts user for the float mutation rate value between 0 and 1 they want the program to run with. If not given proper input, 
        propmts user again. Returns a float.
    """  
    mutation_rate = ""
    while True:
        try:
            mutation_rate = float(input())
            #Ensuring the float is in between 0 and 1
            if mutation_rate < 0 or mutation_rate > 1:
                print("Invalid input, please give a float value between 0 and 1")
                continue
        except ValueError:
            print("Invalid input, please give float value like '.4' or '.6'")
            continue
        else:
            break
    return mutation_rate

def main():
    """
    Main method that runs our Genetic Algorithm system while prompting and outputting information to the user in the terminal shell.
    """
    print ("\nWelecome to CRAIG, brought to you by the team at Too Many Cooks Kitchen. \nCRAIG takes in any known musical artist, scours their songs for any culinary inspiration, \nand then adapts common cookie recipies to have a little taste of fame in them.")
    print ("\nFor each of the following prompts, please input your data and then press 'Return' \n")
    print ("Please input your desired number of generations: ")
    generations_input = get_generations()
    print ("Please input a musical artist. Many artists do not reference food in their songs so don't be detterd if you are unlucky, just keep trying!")
    print ("A few suggestions for good artists include, but are not limited to: Weird Al, Harry Styles, Taylor Swift, Kesha, Katy Perry, and Bruno Mars")
    artist_name = str(input())
    print ("Please input your desired recipe mutation rate (Any value between 0 and 1. The higher value, the greater the odds \nthat your recipe has that extra taste of your favorite star.")
    mutation_intput = get_mutation_rate()
    knowledge_list = []
    lyrics = lyric_gatherer(NUM_ARTIST_SONGS, artist_name)
    song_ingredients = ingredient_matcher(lyrics)
    #Checking to make sure that the Artist input is correct.
    #Issues are if the Artist does not exist, or if they mention no ingredients in their songs.
    while len(song_ingredients) == 0:
        print("We're sorry, the artist you inputted is either not in our database or, more likely, does not sing enough about food. \nPlease try inputting another name!")
        artist_name = str(input())
        lyrics = lyric_gatherer(NUM_ARTIST_SONGS, artist_name)
        song_ingredients = ingredient_matcher(lyrics)
    #Adding all ingredients mentioned by Artist into the knowdlege base as Ingredient objects.
    for item in song_ingredients:
        food = Ingredient(item, 1, "oz")
        knowledge_list.append(food)
    mypop = Population(generations_input, "https://www.tasteofhome.com/collection/the-best-cookie-recipes/", mutation_intput, knowledge_list, artist_name)
    best_recipe = mypop.generate()
    print("We now present for your consumption:\n")
    print (best_recipe)
    print ("And here is its score: " + str(best_recipe.evaluation))

if __name__ == "__main__":
    main()