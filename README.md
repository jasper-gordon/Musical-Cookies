# CRAIG
Cookie
Recipe
Artist
Inspired
Generator

October 15, 2020
By Vincent Dong, Tenzin Choezin and Jasper Gordon

How to run CRAIG : This project is run through the testing_file.py file which when called in a terminal command (python3 testing_file.py) will prompt the user in the terminal shell to input three pieces of data: The desired number of generations for the genetic algorithm proccess, the name of a musical artist, and a value to set the mutation probability. The program will display as it searches through the artist's songs before outputting its resulting best recipe.

Project description: The purpose of this program is to take as an input a given musical artist, then, using the LyricsGenius API, scour the lyrics of their most popular songs in search of any mention of food ingredients. It uses these ingredients to then mutate on a chosen recipe from a given set of base recipes scraped from the web, adding either one of the mentioned ingredients themselves, or looking up a complimentatary ingredient that pairs well and adds that. The program uses a genetic algorithm to generate 10 distinct recipes and then evaluating them to determine the best recipe. This evaluation is done by going through each recipe's ingredients and taking the sum of the pairing value of all possible combinations of ingredients within each recipe. The final score of each recipe is that sum value. By using the unique ingredeints provided by the songs, and by evaluating recipes on how well their ingredients work together, our program creates creative recipes that work despite potentailly unusual pairings. In short, it adds excitement to normal base recipes without giving up flavor cohesivensss.

Limitations: The complexity of CRAIG brought a few issues. We utilized the ingredient flavor pairings database that was provided to us which, whille incredibly helpful in producing a simple, working program, has a limited number of ingredients. This means that some ingredients mentioned by artists may be ignored since they are not known by our database, and thus we have no flavor pairing values for them. Another thing to naivagte was the LyricsGenius API. The API works rather well and includes an impressive database of artists and songs, but takes a significant amount of time. Addtionally, we tried to ensure that our system could handle any given input, and while it does handle most, there are times where giving the API a lesser known artist can cause the API's own system to timeout if too much time has elapsed. This was an issue we investigated but were not able to completely solve. 


Sources: https://towardsdatascience.com/song-lyrics-genius-api-dcc2819c29
        https://www.johnwmillr.com/scraping-genius-lyrics/
        https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
        https://www.digitalocean.com/community/tutorials/how-to-scrape-web-pages-with-beautiful-soup-and-python-3
