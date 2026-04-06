"""_summary_
某次对局的类，包含了这局游戏的所有信息。
"""

from src.base_element.GameMode import CGameMode
from game.Observation import CObservation
from src.base_element.Role import CRole, CRoleUtil
from src.base_element.Stage import CStage
from src.utils.CardUtils import Bombs

class CMatch(object):

    def __init__(self, players):
        # 当前局的状态
        self.card_play_action_seq = [] # 记录每轮玩家出的牌的序列
        self.three_landlord_cards = None
        self.game_over = CStage.PLAYING
        self.acting_player_position = None
        self.players = players
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
        self.bomb_num = 0
        self.last_player = CRole.LANDLORD

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
        self.bomb_num = 0
        self.last_player = CRole.LANDLORD