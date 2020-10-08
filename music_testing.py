#Practice file for music usage

import lyricsgenius
genius = lyricsgenius.Genius("dEVN1E_5EEdG87GGOurKdFhPFkx-k-yTztAOSNJRkutxNoJmX4pI_38cBNPCUDTY")
#genius.verbose = False
genius.remove_section_headers = True
#artist object with songs
#artist = genius.search_artist("pall mat", max_songs = 2, sort = "title")

#List of lyrics for those above songs
#Trying to split up lyrics into individual words
"""
for song in artist.songs:
    full_word_list = song.lyrics.split()
    #Getting rid of duplicate words in list --- Not sure if this is necessary
    unique_word_list = []
    for line in full_word_list:
        if line not in unique_word_list:
            unique_word_list.append(line)
    print (unique_word_list)
    #print (song.lyrics)
    """
#print(artist.songs)



#Ingredient Section

import numpy as np
WORD_EMBED_VALS = np.load('ingred_word_emb.npy', allow_pickle=True).item()
INGRED_CATEGORIES = np.load('ingred_categories.npy', allow_pickle=True).item()
INGREDIENT_LIST = sorted(WORD_EMBED_VALS.keys())

#for i in INGREDIENT_LIST:
    #print (i)

#Method to check if any real ingredients in a song list
#Returns a list of ingredients (strings)
def ingredient_matcher(lyrics):
    real_ingredients = []
    for word in lyrics:
        if word in INGREDIENT_LIST:
            real_ingredients.append(word)
    return real_ingredients

#Gathers the lyrics for given int value of songs of the given artist
#Returns the group of lyrics as a list of strings
def lyric_gatherer(song_limit, artist_name):
    lyric_list = []
    songs = genius.search_artist(artist_name, max_songs = song_limit, sort = "popularity" ).songs
    for song in songs:
        unique_lyrics = []
        unfiltered_lyrics = song.lyrics.split()
        #Only taking unique words from the lyrics to avoid repeats
        for line in unfiltered_lyrics:
            if line not in unique_lyrics:
                #Adjusts case to lower to make sure it is comparable to ingredient_list
                unique_lyrics.append(line.lower())
        #Adding all new unique lyrics to the full list of the artist's lyrics
        lyric_list.extend(unique_lyrics)
    return lyric_list

    
test_list = lyric_gatherer(7, "Jimmy Buffet")
print("Here are the lyrics by Jimmy Buffet that are also known ingredients: ")
print(*ingredient_matcher(test_list), sep = ", ")
