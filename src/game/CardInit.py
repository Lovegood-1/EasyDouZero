import numpy as np
from src.utils.CardUtils import _cards2array, _get_one_hot_array


deck = []
for i in range(3, 15):  # "3" 到 "A"
    deck.extend([i for _ in range(4)])
deck.extend([17 for _ in range(4)])  # "2"
deck.extend([20, 30])  # "X" 和 "D"

def InitCard():
    curDeck = deck.copy()
    np.random.shuffle(curDeck)
    card_play_data = {'landlord': curDeck[:20],
                      'landlord_up': curDeck[20:37],
                      'landlord_down': curDeck[37:54],
                      'three_landlord_cards': curDeck[17:20],
                      }
    for key in card_play_data:
        card_play_data[key].sort()
    return card_play_data