"""
An example of how you could use flavor data to inform your recipe
generation process.  Requires Python v3.

The numpy file format is used because it is more efficient
than reading plain text or CSV files.  You are not restricted to using numpy,
but I would strongly recommend considering how you might handle one or more
large datasets as part of your design process.
"""

import numpy as np

WORD_EMBED_VALS = np.load('ingred_word_emb.npy', allow_pickle=True).item()
INGRED_CATEGORIES = np.load('ingred_categories.npy', allow_pickle=True).item()
INGREDIENT_LIST = sorted(WORD_EMBED_VALS.keys())

def similarity(n1, n2):
    """Returns the similarity between two ingredients based on our data."""
    v1 = WORD_EMBED_VALS[n1]
    v2 = WORD_EMBED_VALS[n2]
    return np.dot(v1, v2)


def pairing(ingr, threshold, cat=None):
    """
    Describes what flavors are similar to the specified ingredient based on
    a similarity threshold and an optional category to which the flavors
    belong.
    """
    pairings = {}
    output = []
    ilist = list(set(INGREDIENT_LIST) - set([ingr]))
    for i in ilist:
        if similarity(ingr, i) >= threshold:
            if cat is not None:
                if i in INGRED_CATEGORIES:
                    if INGRED_CATEGORIES[i] == cat:
                        pairings[i] = similarity(ingr, i)
            else:
                pairings[i] = similarity(ingr, i)
    for key, value in sorted(pairings.items(), key=lambda kv: (kv[1],kv[0]), \
    reverse=True):
        output.append(key)
    output.reverse()   
    #Outputs in order of worst to best
    return output


def request_pairing(ingr, threshold, cat=None):
    """Displays a specific pairing to the user in a readable way."""
    if cat:
        #print("\nWhat pairs well with " + ingr + " that is a " + cat + "?")
        return pairing(ingr, threshold, cat)
    else:
        #print("\nWhat pairs well with " + ingr + "?")
        return pairing(ingr, threshold)


