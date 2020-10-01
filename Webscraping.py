from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys



def scrapeMyAss(url):

    # sets a known browser user agent
    req = Request(url, headers={"User-Agent": "Chrome"})
    source = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(source, 'html.parser')
    #print(soup.prettify())

    link_list = []
    for section in soup.findAll('div', {"class": "listicle-page__cta-button"}):
        for link in section.findAll('a'):
            link_list.append(link.get('href'))
    
    recipe_list = []

    req = Request(link_list[0], headers={"User-Agent": "Chrome"})
    source = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(source, 'html.parser')
    
    """recipe = soup.find('ul', {"class": "recipe-ingredients__list recipe-ingredients__collection splitColumns"})
    ingredient_list = []
    for ingredient in recipe:
        ingredient_list.append(ingredient.text)
    print(ingredient_list)"""

    for i in range(20):

        req = Request(link_list[i], headers={"User-Agent": "Chrome"})
        source = urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(source, 'html.parser')

        ingredient_list = []

        for recipe in soup.find('ul', {"class": "recipe-ingredients__list recipe-ingredients__collection splitColumns"}):
            
            for ingredient in recipe:
                
                ingredient_list.append(str(ingredient))
        

        recipe_list.append(ingredient_list)
    
    print(type(recipe_list[1][1]))
    print(recipe_list)

def main():

    scrapeMyAss(sys.argv[1])

if __name__ == "__main__":
    main()