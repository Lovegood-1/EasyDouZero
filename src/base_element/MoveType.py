from enum import Enum, auto
import itertools

class CMoveType(Enum):
    TYPE_0_PASS           = auto()
    TYPE_1_SINGLE         = auto()
    TYPE_2_PAIR           = auto()
    TYPE_3_TRIPLE         = auto()
    TYPE_4_BOMB           = auto()
    TYPE_5_KING_BOMB      = auto()
    TYPE_6_3_1            = auto()
    TYPE_7_3_2            = auto()
    TYPE_8_SERIAL_SINGLE  = auto()
    TYPE_9_SERIAL_PAIR    = auto()
    TYPE_10_SERIAL_TRIPLE = auto()
    TYPE_11_SERIAL_3_1    = auto()
    TYPE_12_SERIAL_3_2    = auto()
    TYPE_13_4_2           = auto()
    TYPE_14_4_22          = auto()
    TYPE_15_WRONG         = auto()

# global parameters
MIN_SINGLE_CARDS = 5
MIN_PAIRS = 3
MIN_TRIPLES = 2

# return all possible results of selecting num cards from cards list
def select(cards, num):
    return [list(i) for i in itertools.combinations(cards, num)]
