from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from src.base_element.Role import CRole
@dataclass
class CObservation:
    """
    The game state is described as infoset, which
    includes all the information in the current situation,
    such as the hand cards of the three players, the
    historical moves, etc.
    """
    # def __init__(self, player_position):
    #     # The player position, i.e., landlord, landlord_down, or landlord_up
    #     self.player_position = player_position
    #     # The hand cands of the current player. A list.
    #     self.player_hand_cards = None
    #     # The number of cards left for each player. It is a dict with str-->int 
    #     self.num_cards_left_dict = None
    #     # The three landload cards. A list.
    #     self.three_landlord_cards = None
    #     # The historical moves. It is a list of list
    #     self.card_play_action_seq = None
    #     # The union of the hand cards of the other two players for the current player 
    #     self.other_hand_cards = None
    #     # The legal actions for the current move. It is a list of list
    #     self.legal_actions = None
    #     # The most recent valid move
    #     self.last_move = None
    #     # The most recent two moves
    #     self.last_two_moves = None
    #     # The last moves for all the postions
    #     self.last_move_dict = None
    #     # The played cands so far. It is a list.
    #     self.played_cards = None
    #     # The hand cards of all the players. It is a dict. 
    #     self.all_handcards = None
    #     # Last player position that plays a valid move, i.e., not `pass`
    #     self.last_pid = None
    #     # The number of bombs played so far
    #     self.bomb_num = None
    player_position: CRole
    player_hand_cards : List[int]
    num_cards_left_dict : Dict[str, int]
    three_landlord_cards : List[int]
    card_play_action_seq : List[List[int]]
    other_hand_cards : List[int]
    legal_actions : List[List[int]]
    last_move : Optional[List[int]]
    last_two_moves : Optional[List[List[int]]]
    last_move_dict : Dict[CRole, List[int]]
    played_cards : List[int]
    all_handcards : Dict[CRole, List[int]]
    last_player : Optional[CRole]
    bomb_num : int
    legal_action : List[Any] # 用具体类型
