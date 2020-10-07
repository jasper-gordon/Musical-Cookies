from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys
from Ingredient import Ingredient
from Recipe import Recipe



def web_scraper(url):

    # sets a known browser user agent
    req = Request(url, headers={"User-Agent": "Chrome"})
    source = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(source, 'html.parser')
    #print(soup.prettify())

    link_list = []
    for section in soup.findAll('div', {"class": "listicle-page__cta-button"}):
        for link in section.findAll('a'):
            link_list.append(link.get('href'))

    """req = Request(link_list[0], headers={"User-Agent": "Chrome"})
    source = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(source, 'html.parser')"""

    
    
    """recipe = soup.find('ul', {"class": "recipe-ingredients__list recipe-ingredients__collection splitColumns"})
    ingredient_list = []
    for ingredient in recipe:
        ingredient_list.append(ingredient.text)
    print(ingredient_list)"""

    ingredient_dict = {}
    
    for i in range(10):

        req = Request(link_list[i], headers={"User-Agent": "Chrome"})
        source = urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(source, 'html.parser')

        
        ingredient_list = []
        
        recipe_name = str(soup.find('h1', {"class": "recipe-title"}).text)

        for recipe in soup.find('ul', {"class": "recipe-ingredients__list recipe-ingredients__collection splitColumns"}):
            
            for ingredient in recipe:

                if ingredient != soup.find('b', {"class": "sIngredient"}):
                    ingredient_list.append(str(ingredient))
        
        ingredient_dict[recipe_name] = ingredient_list
    
    #print(type(recipe_list[1][1]))
    #print(recipe_list)
    print("Webscraper was called")
    print(ingredient_dict)
    return ingredient_dict

def main():

    web_scraper(sys.argv[1])

if __name__ == "__main__":
    main()