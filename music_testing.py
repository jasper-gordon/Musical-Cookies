#Practice file for music usage

import lyricsgenius
genius = lyricsgenius.Genius("dEVN1E_5EEdG87GGOurKdFhPFkx-k-yTztAOSNJRkutxNoJmX4pI_38cBNPCUDTY")
genius.verbose = False
genius.remove_section_headers = True
#artist object with songs
artist = genius.search_artist("Tom Petty", max_songs = 2, sort = "title")

#List of lyrics for those above songs
#Trying to split up lyrics into individual words
for song in artist.songs:
    full_word_list = song.lyrics.split()
    #Getting rid of duplicate words in list --- Not sure if this is necessary
    unique_word_list = []
    for line in full_word_list:
        if line not in unique_word_list:
            unique_word_list.append(line)
    print (unique_word_list)
    #print (song.lyrics)
    
#print(artist.songs)


#Ingredient Section

import numpy as np
WORD_EMBED_VALS = np.load('ingred_word_emb.npy', allow_pickle=True).item()
INGRED_CATEGORIES = np.load('ingred_categories.npy', allow_pickle=True).item()
INGREDIENT_LIST = sorted(WORD_EMBED_VALS.keys())

print("Second ingredient " + INGREDIENT_LIST[1])

