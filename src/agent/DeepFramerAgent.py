import numpy as np

from src.base_element.Agent import CAgent
from src.base_element.Record import CRecord
from src.base_element.Role import CRole
from src.utils.CardUtils import _cards2array, _get_one_hot_array, _process_action_seq, _action_seq_list2array

class CDeepFramerAgent(CAgent):

    def __init__(self, role: CRole):
        super().__init__()
        self.name = 'DeepFramerAgent'
        self.role = role

    def select_action(self, player ,legal_actions, records: CRecord):
        input_z = torch.from_numpy(self._get_z_batch(player, legal_actions, records)).float()
        input_x = torch.from_numpy(self._get_x_batch(player, legal_actions,records)).float()
        pred = self.model.forward(input_z, input_x).detach().numpy()
        best_action_index = np.argmax(pred, axis=0)[0]
        return legal_actions[best_action_index]


    def _get_x_batch(self, player, legal_actions, records: CRecord):
        # 这里可以根据 legal_actions 和 records 的结构设计输入 z_batch 的格式
        # 例如，可以将 legal_actions 转换为一个适合模型输入的张量，并结合 records 中的游戏状态信息进行处理
        # 具体的转换逻辑需要根据 legal_actions 和 CRecord 的定义来实现
        num_legal_actions = len(legal_actions)
        hand_cards = _cards2array(player.hand_cards)
        hand_cards_batch = np.repeat(hand_cards[np.newaxis, :],
                                    num_legal_actions, axis=0)
        
        other_hand_cards = []
        if player.role == CRole.LANDLORD:
            other_hand_cards = records.other_hand_cards[CRole.LANDLORD_UP] + records.other_hand_cards[CRole.LANDLORD_DOWN]
        elif player.role == CRole.LANDLORD_UP:
            other_hand_cards = records.other_hand_cards[CRole.LANDLORD] + records.other_hand_cards[CRole.LANDLORD_DOWN]
        elif player.role == CRole.LANDLORD_DOWN:
            other_hand_cards = records.other_hand_cards[CRole.LANDLORD] + records.other_hand_cards[CRole.LANDLORD_UP]
        other_hand_cards = _cards2array(other_hand_cards)
        other_hand_cards_batch = np.repeat(other_hand_cards[np.newaxis, :],
                                        num_legal_actions, axis=0)
        
        last_action = _cards2array(records.last_played_cards['cards'])
        last_action_batch = np.repeat(last_action[np.newaxis, :],
                                    num_legal_actions, axis=0)
        
        legal_actions_batch = np.zeros(hand_cards_batch.shape)
        for j, action in enumerate(legal_actions):
            legal_actions_batch[j] = _cards2array(action)

        landlord_num_cards_left = _get_one_hot_array(records.num_cards_left_dicts[CRole.LANDLORD], 20)
        landlord_num_cards_left_batch = np.repeat(landlord_num_cards_left[np.newaxis, :],
                                                num_legal_actions, axis=0)
        
        landlord_played_cards = _cards2array(records.played_cards[CRole.LANDLORD])
        landlord_played_cards_batch = np.repeat(landlord_played_cards[np.newaxis, :],
                                                num_legal_actions, axis=0)
        if player.role == CRole.LANDLORD_UP:
            landlord_others_played_cards = _cards2array(records.played_cards[CRole.LANDLORD_DOWN])
            landlord_others_played_cards_batch = np.repeat(landlord_others_played_cards[np.newaxis, :],
                                                    num_legal_actions, axis=0)
            landlord_others_num_cards_left = _get_one_hot_array(records.num_cards_left_dicts[CRole.LANDLORD_DOWN], 17)
            landlord_others_num_cards_left_batch = np.repeat(landlord_others_num_cards_left[np.newaxis, :],
                                                    num_legal_actions, axis=0)
        else:
            landlord_others_played_cards = _cards2array(records.played_cards[CRole.LANDLORD_UP])
            landlord_others_played_cards_batch = np.repeat(landlord_others_played_cards[np.newaxis, :],
                                                    num_legal_actions, axis=0)
            landlord_others_num_cards_left = _get_one_hot_array(records.num_cards_left_dicts[CRole.LANDLORD_UP], 17)
            landlord_others_num_cards_left_batch = np.repeat(landlord_others_num_cards_left[np.newaxis, :],
                                                    num_legal_actions, axis=0)

        return np.hstack((
            hand_cards_batch,
            other_hand_cards_batch,
            last_action_batch,
            landlord_played_cards_batch,
            landlord_others_played_cards_batch,
            landlord_num_cards_left_batch,
            landlord_others_num_cards_left_batch,
            legal_actions_batch
        ))

     
    def _get_z_batch(self, player, legal_actions, records: CRecord):
        # 这里可以根据 legal_actions 和 records 的结构设计输入 x_batch 的格式
        # 例如，可以将 legal_actions 转换为一个适合模型输入的张量，并结合 records 中的游戏状态信息进行处理
        # 具体的转换逻辑需要根据 legal_actions 和 CRecord 的定义来实现
        z = _action_seq_list2array(_process_action_seq(records.card_play_action_seq))
        z_batch = np.repeat(z[np.newaxis, :],
                            len(legal_actions), axis=0)
        return z_batch

