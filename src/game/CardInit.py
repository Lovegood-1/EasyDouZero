import numpy as np

Card2Column = {3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7,
               11: 8, 12: 9, 13: 10, 14: 11, 17: 12}


EnvCard2RealCard = {3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q',
                    13: 'K', 14: 'A', 17: '2', 20: 'X', 30: 'D'}

RealCard2EnvCard = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                    '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
                    'K': 13, 'A': 14, '2': 17, 'X': 20, 'D': 30}

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