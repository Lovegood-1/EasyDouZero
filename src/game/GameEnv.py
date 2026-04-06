"""_summary_
整个游戏环境类，包含了游戏几乎所有的状态信息。
"""

from game.Match import CMatch
from src.base_element.GameMode import CGameMode
from game.Observation import CObservation
from src.base_element.Role import CRole, CRoleUtil
from src.base_element.Stage import CStage
from src.utils.CardUtils import Bombs

class CGameEnv(object):

    def __init__(self, mode, players):

        # 游戏模式：sandbox or competition
        self.mode = mode

        # 当前局的状态
        self.match = CMatch(players)

        # 所有局的统计信息
        self.num_wins = {CRole.LANDLORD     : 0,
                         CRole.LANDLORD_UP  : 0,
                         CRole.LANDLORD_DOWN: 0}
        self.num_scores = {CRole.LANDLORD     : 0,
                           CRole.LANDLORD_UP  : 0,
                           CRole.LANDLORD_DOWN: 0}
        self.bomb_num = 0

    def step(self):
        action = self.players[self.acting_player_position].act(
            self.game_infoset)
        assert action in self.game_infoset.legal_actions

        if len(action) > 0:
            self.last_player = self.acting_player_position
        self.bomb_num += 1 if action in Bombs else 0

        self.last_move_dict[
            self.acting_player_position] = action.copy()

        self.card_play_action_seq.append(action)
        self.update_acting_player_hand_cards(action)

        self.played_cards[self.acting_player_position] += action

        if self.acting_player_position == CRole.LANDLORD and \
                len(action) > 0 and \
                len(self.three_landlord_cards) > 0:
            for card in action:
                if len(self.three_landlord_cards) > 0:
                    if card in self.three_landlord_cards:
                        self.three_landlord_cards.remove(card)
                else:
                    break

        self.game_done()
        if self.game_over == CStage.PLAYING:
            # self.get_acting_player_position()
            self.acting_player_position = CRoleUtil.get_next_role(
                self.acting_player_position)
            self.game_infoset = self.get_infoset()


    def card_play_init(self, card_play_data):
        self.role_observation['landlord'].player_hand_cards = \
            card_play_data['landlord']
        self.role_observation['landlord_up'].player_hand_cards = \
            card_play_data['landlord_up']
        self.role_observation['landlord_down'].player_hand_cards = \
            card_play_data['landlord_down']
        self.three_landlord_cards = card_play_data['three_landlord_cards']
        self.acting_player_position = CRole.LANDLORD
        self.game_infoset = self.get_infoset()

    def game_done(self):
        if len(self.role_observation['landlord'].player_hand_cards) == 0 or \
                len(self.role_observation['landlord_up'].player_hand_cards) == 0 or \
                len(self.role_observation['landlord_down'].player_hand_cards) == 0:
            # if one of the three players discards his hand, game is over.
            self.update_num_wins_scores()
            self.game_over = CStage.GAME_OVER
 
    def update_num_wins_scores(self):
        if len(self.role_observation['landlord'].player_hand_cards) == 0:
            dictScore = {'landlord': 2,
                        'farmer': -1}
        else:
            dictScore = {'landlord': -2,
                        'farmer': 1}
        for pos, utility in dictScore.items():
            base_score = 2 if pos == 'landlord' else 1
            if utility > 0:
                self.num_wins[pos] += 1
                self.winner = pos
                self.num_scores[pos] += base_score * (2 ** self.bomb_num)
            else:
                self.num_scores[pos] -= base_score * (2 ** self.bomb_num)

    def get_winner(self):
        return self.winner

    def get_bomb_num(self):
        return self.bomb_num


    def get_last_move(self):
        last_move = []
        if len(self.card_play_action_seq) != 0:
            if len(self.card_play_action_seq[-1]) == 0:
                last_move = self.card_play_action_seq[-2]
            else:
                last_move = self.card_play_action_seq[-1]

        return last_move

    def get_last_two_moves(self):
        last_two_moves = [[], []]
        for card in self.card_play_action_seq[-2:]:
            last_two_moves.insert(0, card)
            last_two_moves = last_two_moves[:2]
        return last_two_moves

    def get_acting_player_position(self):
        self.acting_player_position = CRoleUtil.get_next_role(
            self.acting_player_position)

        return self.acting_player_position

    def update_acting_player_hand_cards(self, action):
        if action != []:
            for card in action:
                self.role_observation[
                    self.acting_player_position].player_hand_cards.remove(card)
            self.role_observation[self.acting_player_position].player_hand_cards.sort()

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

    def reset(self):
        self.card_play_action_seq = []
        self.three_landlord_cards = None
        self.game_over = CStage.PLAYING
        self.acting_player_position = None
        self.last_move_dict = {CRole.LANDLORD     : [],
                               CRole.LANDLORD_UP  : [],
                               CRole.LANDLORD_DOWN: []}
        self.played_cards = {CRole.LANDLORD     : [],
                             CRole.LANDLORD_UP  : [],
                             CRole.LANDLORD_DOWN: []}
        self.role_observation = {
            CRole.LANDLORD     : CObservation(),
            CRole.LANDLORD_UP  : CObservation(),
            CRole.LANDLORD_DOWN: CObservation()}
        self.last_player = CRole.LANDLORD

    def get_infoset(self):
        pass