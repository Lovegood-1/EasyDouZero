"""_summary_
某次对局的类，包含了这局游戏的所有信息。
"""
import numpy as np

from base_element.Observation import CObservation
from src.base_element.Role import CRole
from src.base_element.Stage import CStage
Roles = (CRole.LANDLORD, CRole.LANDLORD_UP, CRole.LANDLORD_DOWN)
 
class CMatch(object):
    DECK = tuple([i for i in range(3, 15) for _ in range(4)] + [17] * 4 + [20, 30])

    def __init__(self, players):
        self.players = players
        self._init_state()

    def reset(self):
        self._init_state()

    def step(self, role, action):
        assert role == self.acting_player_position
        assert action in self.legal_actions
        self.last_player = role if len(action) > 0 else self.last_player
        self.bomb_num += 1 if action in Bombs else 0
        self.last_move_dict[role] = action.copy()
        self.card_play_action_seq.append(action)
        self.played_cards[role] += action

        self._update_role_hand_cards(action)
        self._update_three_landlord_cards(action)
        self._update_stage(action)

        if self.stage != CStage.GAME_OVER:
            self._update_role(role)

    def get_observation(self, role: CRole) -> CObservation:
        pass


    def get_last_two_moves(self):
        last_two_moves = [[], []]
        for card in self.card_play_action_seq[-2:]:
            last_two_moves.insert(0, card)
            last_two_moves = last_two_moves[:2]
        return last_two_moves

    def get_last_move(self):
        last_move = []
        if len(self.card_play_action_seq) != 0:
            if len(self.card_play_action_seq[-1]) == 0:
                last_move = self.card_play_action_seq[-2]
            else:
                last_move = self.card_play_action_seq[-1]

        return last_move

    def get_legal_card_play_actions(self):
        mg = MovesGener(
            self.role_observation[self.acting_player_position].player_hand_cards)

        action_sequence = self.card_play_action_seq

        rival_move = []
        if len(action_sequence) != 0:
            if len(action_sequence[-1]) == 0:
                rival_move = action_sequence[-2]
            else:
                rival_move = action_sequence[-1]

        rival_type = md.get_move_type(rival_move)
        rival_move_type = rival_type['type']
        rival_move_len = rival_type.get('len', 1)
        moves = list()

        if rival_move_type == md.TYPE_0_PASS:
            moves = mg.gen_moves()

        elif rival_move_type == md.TYPE_1_SINGLE:
            all_moves = mg.gen_type_1_single()
            moves = ms.filter_type_1_single(all_moves, rival_move)

        elif rival_move_type == md.TYPE_2_PAIR:
            all_moves = mg.gen_type_2_pair()
            moves = ms.filter_type_2_pair(all_moves, rival_move)

        elif rival_move_type == md.TYPE_3_TRIPLE:
            all_moves = mg.gen_type_3_triple()
            moves = ms.filter_type_3_triple(all_moves, rival_move)

        elif rival_move_type == md.TYPE_4_BOMB:
            all_moves = mg.gen_type_4_bomb() + mg.gen_type_5_king_bomb()
            moves = ms.filter_type_4_bomb(all_moves, rival_move)

        elif rival_move_type == md.TYPE_5_KING_BOMB:
            moves = []

        elif rival_move_type == md.TYPE_6_3_1:
            all_moves = mg.gen_type_6_3_1()
            moves = ms.filter_type_6_3_1(all_moves, rival_move)

        elif rival_move_type == md.TYPE_7_3_2:
            all_moves = mg.gen_type_7_3_2()
            moves = ms.filter_type_7_3_2(all_moves, rival_move)

        elif rival_move_type == md.TYPE_8_SERIAL_SINGLE:
            all_moves = mg.gen_type_8_serial_single(repeat_num=rival_move_len)
            moves = ms.filter_type_8_serial_single(all_moves, rival_move)

        elif rival_move_type == md.TYPE_9_SERIAL_PAIR:
            all_moves = mg.gen_type_9_serial_pair(repeat_num=rival_move_len)
            moves = ms.filter_type_9_serial_pair(all_moves, rival_move)

        elif rival_move_type == md.TYPE_10_SERIAL_TRIPLE:
            all_moves = mg.gen_type_10_serial_triple(repeat_num=rival_move_len)
            moves = ms.filter_type_10_serial_triple(all_moves, rival_move)

        elif rival_move_type == md.TYPE_11_SERIAL_3_1:
            all_moves = mg.gen_type_11_serial_3_1(repeat_num=rival_move_len)
            moves = ms.filter_type_11_serial_3_1(all_moves, rival_move)

        elif rival_move_type == md.TYPE_12_SERIAL_3_2:
            all_moves = mg.gen_type_12_serial_3_2(repeat_num=rival_move_len)
            moves = ms.filter_type_12_serial_3_2(all_moves, rival_move)

        elif rival_move_type == md.TYPE_13_4_2:
            all_moves = mg.gen_type_13_4_2()
            moves = ms.filter_type_13_4_2(all_moves, rival_move)

        elif rival_move_type == md.TYPE_14_4_22:
            all_moves = mg.gen_type_14_4_22()
            moves = ms.filter_type_14_4_22(all_moves, rival_move)

        if rival_move_type not in [md.TYPE_0_PASS,
                                   md.TYPE_4_BOMB, md.TYPE_5_KING_BOMB]:
            moves = moves + mg.gen_type_4_bomb() + mg.gen_type_5_king_bomb()

        if len(rival_move) != 0:  # rival_move is not 'pass'
            moves = moves + [[]]

        for m in moves:
            m.sort()

        return moves

    def _init_state(self):
        self.card_play_action_seq = []  # 记录每轮玩家出的牌的序列
        self.three_landlord_cards, self.dictHandcards = CMatch._init_handcards()
        self.stage = CStage.PLAYING
        self.acting_player_position = None
        self.last_move_dict = {r: [] for r in Roles}
        self.played_cards = {r: [] for r in Roles}
        self.role_observation = {r: CObservation() for r in Roles}
        self.bomb_num = 0
        self.last_player = CRole.LANDLORD
        self.dictHandcards = {r: [] for r in Roles}

    def _update_stage(self, action):
        if len(self.dictHandcards[self.acting_player_position]) == 0:
            self.stage = CStage.GAME_OVER

    def _update_role_hand_cards(self, action):
        if action:
            for card in action:
                self.dictHandcards[self.acting_player_position].remove(card)
            self.dictHandcards[self.acting_player_position].sort()

    def _update_three_landlord_cards(self, action):
        if self.acting_player_position == CRole.LANDLORD and \
                len(action) > 0 and \
                len(self.three_landlord_cards) > 0:
            for card in action:
                if len(self.three_landlord_cards) > 0 and card in self.three_landlord_cards:
                    self.three_landlord_cards.remove(card)
                else:
                    break

    def _update_role(self, role):
        self.acting_player_position = CRoleUtil.get_next_role(
            self.acting_player_position)
        

    @staticmethod
    def _init_handcards():
        deck = CMatch.DECK.copy()
        np.random.shuffle(deck)
        handCards = {
            CRole.LANDLORD: deck[:20],
            CRole.LANDLORD_UP: deck[20:37],
            CRole.LANDLORD_DOWN: deck[37:54],
        }
        three_landlord_cards = deck[17:20]
        return handCards, three_landlord_cards

