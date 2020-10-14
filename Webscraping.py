"""Names: Vincent Dong, Tenzin Choezin, Jasper Gordon
Course: CSCI 3725
Assignment: PQ2
Date: 08/13/2020
Description: This file handles the web scraping needed to build our inspiring set of known cookie recipes.
        Given a specific url of the top 50 cookie recipes from the Taste of Home website, it takes the first
        10 recipes and stores them into a dictioinary with the name of the recipe as the key and a list of
        its ingredients as the value."""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys
from Ingredient import Ingredient
from Recipe import Recipe



def web_scraper(url):
    """ 
    Takes a url of the website where we extract our recipes from to construct an inspiring set of known cookie recipes.
        This method is only formatted for extracting recipes from a specific website, so any other website will not
        work. This function returns a dictionary with the recipe's name as the key and the list of its ingredients as
        the value.
    """

    # create a Request object that sets a known browser user agent
    req = Request(url, headers={"User-Agent": "Chrome"})

    # opens the url within req and turns it into a readable format
    source = urlopen(req).read().decode('utf-8')

    # create a Beautiful Soup object
    soup = BeautifulSoup(source, 'html.parser')
    
    # list of url links to different recipes
    link_list = []

    # loop through the html of the website and find all the div tags with the specified class
    for section in soup.findAll('div', {"class": "listicle-page__cta-button"}):
        # loop through all the a tags in each section to find the links to specific recipes
        for link in section.findAll('a'):
            # add the link to the link list
            link_list.append(link.get('href'))

    # stores the recipe name as the key and a list of the recipe's ingredients as the value
    ingredient_dict = {}
    
    for i in range(10):

        ingredient_dict_constructor(link_list, i, ingredient_dict)
    
    return ingredient_dict

def ingredient_dict_constructor(link_list, i, ingredient_dict):
    """
    Takes the list of links to specific recipes, the ingredient dictionary of recipes and the iteration number of the for loop.
        This method accesses each specific link in the link list and stores all of the ingredients in the recipe into a list.
        That list is then stored as the value in the ingredient dictionary while the name of that recipe is the key for it.
        This function builds the ingredient dictionary.
    """
    
    # create a Request object that sets a known browser user agent
    req = Request(link_list[i], headers={"User-Agent": "Chrome"})

    # opens the url within req and turns it into a readable format
    source = urlopen(req).read().decode('utf-8')

    # create a Beautiful Soup object
    soup = BeautifulSoup(source, 'html.parser')


    ingredient_list = []

    recipe_name = str(soup.find('h1', {"class": "recipe-title"}).text)

    # access the recipes
    for recipe in soup.find('ul', {"class": "recipe-ingredients__list recipe-ingredients__collection splitColumns"}):

        for ingredient in recipe:

            # makes sure we get actual ingredients added to the ingredient list
            if ingredient != soup.find('b', {"class": "sIngredient"}):
                ingredient_list.append(str(ingredient))

    ingredient_dict[recipe_name] = ingredient_list

def main():

    web_scraper(sys.argv[1])

if __name__ == "__main__":
    main()