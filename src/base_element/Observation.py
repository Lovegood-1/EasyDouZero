import numpy as np
from src.base_element.Role import CRole

class CObservation:
    def __init__(self, role, legal_actions,  hand_cards, other_hand_cards, last_action, landlord_up_cards_left, landlord_cards_left, landlord_down_cards_left):
        self.role = role
        self.legal_actions = legal_actions
        self.other_hand_cards = other_hand_cards
        self.hand_cards = hand_cards
        self.last_action = last_action
        self.landlord_up_cards_left = landlord_up_cards_left
        self.landlord_cards_left = landlord_cards_left
        self.landlord_down_cards_left = landlord_down_cards_left
        self.landlord_up_played_cards = landlord_up_played_cards
        self.landlord_played_cards = landlord_played_cards
        self.landlord_down_played_cards = landlord_down_played_cards



def ConvertToRoleObservation(role, legal_actions, records: CRecord, hand_cards):
    # 这里可以根据玩家的角色、合法动作、游戏记录和手牌信息构建一个观察对象
    # 例如，可以提取玩家的手牌、出牌历史、当前牌面等信息，并进行适当的编码
    # 具体的转换逻辑需要根据 CRecord 的定义来实现
    num_legal_actions = len(legal_actions)
    hand_cards = _cards2array(hand_cards)
    hand_cards_batch = np.repeat(hand_cards[np.newaxis, :],
                                num_legal_actions, axis=0)
    
    other_hand_cards = []
    if role == CRole.LANDLORD:
        other_hand_cards = records.other_hand_cards[CRole.LANDLORD_UP] + records.other_hand_cards[CRole.LANDLORD_DOWN]
    elif role == CRole.LANDLORD_UP:
        other_hand_cards = records.other_hand_cards[CRole.LANDLORD] + records.other_hand_cards[CRole.LANDLORD_DOWN]
    elif role == CRole.LANDLORD_DOWN:
        other_hand_cards = records.other_hand_cards[CRole.LANDLORD] + records.other_hand_cards[CRole.LANDLORD_UP]
    other_hand_cards = _cards2array(other_hand_cards)
    other_hand_cards_batch = np.repeat(other_hand_cards[np.newaxis, :],
                                     num_legal_actions, axis=0)
    
    last_action = _cards2array(records.last_played_cards['cards'])
    last_action_batch = np.repeat(last_action[np.newaxis, :],
                                num_legal_actions, axis=0)
    
 
    legal_actions_array = np.zeros(hand_cards_batch.shape)
    for j, action in enumerate(legal_actions):
        legal_actions_array[j] = _cards2array(action)

    landlord_up_cards_left = _get_one_hot_array(records.num_cards_left_dicts[CRole.LANDLORD_UP], 17)
    landlord_up_cards_left_batch = np.repeat(landlord_up_cards_left[np.newaxis, :],
                                            num_legal_actions, axis=0)
    landlord_down_cards_left = _get_one_hot_array(records.num_cards_left_dicts[CRole.LANDLORD_DOWN], 17)
    landlord_down_cards_left_batch = np.repeat(landlord_down_cards_left[np.newaxis, :],
                                            num_legal_actions, axis=0)
    landlord_cards_left = _get_one_hot_array(records.num_cards_left_dicts[CRole.LANDLORD], 20)
    landlord_cards_left_batch = np.repeat(landlord_cards_left[np.newaxis, :],
                                            num_legal_actions, axis=0)
    
    