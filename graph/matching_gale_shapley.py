import math
from graph_package.flow_graph import FlowGraph
import pandas as pd
from collections import defaultdict

# def better_choise(man, woman, mates, preferred_rankings_women):
#     curr_man_rank = preferred_rankings_women[woman]

def gale_shapely(preferred_rankings_men, preferred_rankings_women):
    free_mens = list(preferred_rankings_men.keys())
    mates = {}

    while free_mens:
        for man in free_mens:
            top_women =  preferred_rankings_men[man].pop(0)
            if top_women not in mates or is_better_mate(man, top_women, preferred_rankings_women):
                mates[top_women] = man
                free_mens.remove(man)
            else:
                del preferred_rankings_men[man][prefered_woman]

if __name__ == '__main__':
    preferred_rankings_men = {
        'alex': ['alice', 'brenda', 'carrol', 'joana'],
        'bob': ['carrol', 'joana', 'alice', 'brenda'],
        'collin': ['joana', 'carrol', 'brenda', 'alice'],
        'john': ['joana', 'alice', 'alice', 'brenda']
    }

    preferred_rankings_women = {
        'alice': ['bob', 'alex', 'collin', 'john'],
        'brenda': ['john', 'bob', 'alex', 'collin'],
        'carrol': ['alex', 'bob', 'collin', 'john'],
        'joana': ['alex', 'john', 'collin', 'bob']
    }

    print(preferred_rankings_men)
    poper = preferred_rankings_men['alex'].pop(0)
    print(preferred_rankings_men)
