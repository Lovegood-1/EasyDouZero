"""_summary_
整个游戏环境类，包含了游戏几乎所有的状态信息。
"""

from game.Match import CMatch
from src.base_element.GameMode import CGameMode
from base_element.Observation import CObservation
from src.base_element.Role import CRole, CRoleUtil
from src.base_element.Stage import CStage
from src.utils.CardUtils import Bombs

class CGameEnv(object):

    def __init__(self, mode, players: dict):

        # 游戏模式：sandbox or competition
        self.mode = mode

        # 当前局的状态
        self.match = CMatch(players)
        self.players = players

        # 所有局的统计信息
        self.num_wins = {CRole.LANDLORD     : 0,
                         CRole.LANDLORD_UP  : 0,
                         CRole.LANDLORD_DOWN: 0}
        self.num_scores = {CRole.LANDLORD     : 0,
                           CRole.LANDLORD_UP  : 0,
                           CRole.LANDLORD_DOWN: 0}

    def step(self):
        # self.update_observations()
        player_obs = self.match.get_observation(self.match.acting_player_position)
        action = self.players[self.match.acting_player_position].act(player_obs)
        self.match.step(self.match.acting_player_position, action)

        if self.mode == CGameMode.SANDBOX:
            listPlayer = [CRole.LANDLORD, CRole.LANDLORD_UP, CRole.LANDLORD_DOWN]
        else:
            listPlayer = [self.match.acting_player_position]

        listObs = [self.match.get_observation(pos) for pos in listPlayer]
        Done = self.match.stage == CStage.GAME_OVER

        return listObs, Done
 
    def update_num_wins_scores(self):
        if len(self.match.dictHandcards[CRole.LANDLORD]) == 0:
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

    def reset(self):
        self.match.reset()