from src.base_element.GameMode import CGameMode
from src.base_element.EnvState import CEnvState
from src.game.CardInit import InitCard
from src.base_element.Role import CRole
from src.move.generate import gen_moves_by_hand_cards_and_trival

class CEnv(object):

    def __init__(self, mode: CGameMode, players: dict):
        # 游戏模式：sandbox or competition
        self.mode = mode
        self.players = players
        
        # 初始状态为 IDLE
        self.state = CEnvState.IDLE
        # 游戏状态变量在 start() 中初始化
        self.step_count = None


    def start(self):
        """游戏开始，进行发牌等初始化步骤
        
        Raises:
            RuntimeError: 如果游戏已经开始（状态不是 IDLE）
        """
        if self.state != CEnvState.IDLE:
            raise RuntimeError(f"无法开始游戏：当前状态为 {self.state.name}，只能从 IDLE 状态开始游戏")
        
        print("游戏开始，正在发牌...")
        # 初始化游戏状态
        self.step_count = 0
        self.state = CEnvState.PLAYING
        self.current_player = CRole.LANDLORD
        self.last_play_cards = {'role': None, 'cards': []}  # 记录上次出牌的玩家角色和牌
        self._init_hand_cards()

    def step(self, action):
        """游戏进行一步，玩家出牌等
        
        Raises:
            RuntimeError: 如果游戏未开始或已结束
        """
        if self.state != CEnvState.PLAYING:
            raise RuntimeError(f"无法执行步骤：当前状态为 {self.state.name}，只能在 PLAYING 状态执行步骤")
        
        legal_actions = self.cur_legal_actions()
        assert action in legal_actions, f"玩家 {self.current_player} 的出牌 {action} 不合法，合法出牌列表: {legal_actions}"
        
        # Update: 修改环境状态，例如记录玩家出牌、切换到下一个玩家等
        self._update_hand_cards(self.current_player, action)

        if self._check_game_over():
            print(f"游戏结束，正在结算...，胜利者是：{self.current_player}")  # 这里可以根据实际逻辑确定胜利者角色
            self._set_game_over()
            return

        if action:  # 如果玩家出牌不为空，则更新 last_play_cards
            self.last_play_cards = {'role': self.current_player, 'cards': action}  # 这里可以根据实际逻辑更新玩家出的牌
        self.current_player = self._next_player(self.current_player)

    def end(self):
        """判断游戏是否结束
        
        Returns:
            bool: 游戏是否已结束
        """
        return self.state == CEnvState.GAME_OVER
    
    def cur_legal_actions(self):
        """获取当前玩家的合法出牌列表
        
        Returns:
            list: 当前玩家可以出的牌的列表
        """

        rival_cards = []
        if self.last_play_cards['role'] is not None and self.last_play_cards['role'] != self.current_player:
            rival_cards = self.last_play_cards['cards']
        return gen_moves_by_hand_cards_and_trival(hand_cards=self.players[self.current_player].hand_cards, rival_cards=rival_cards)

    def _init_hand_cards(self):
        """初始化玩家手牌 """
        dict_cards = InitCard()
        self.players[CRole.LANDLORD].hand_cards = dict_cards['landlord']
        self.players[CRole.LANDLORD_UP].hand_cards = dict_cards['landlord_up']
        self.players[CRole.LANDLORD_DOWN].hand_cards = dict_cards['landlord_down']

        # 地主玩家获得底牌
        self.three_landlord_cards = dict_cards['three_landlord_cards']  # 三张底牌

    def _check_game_over(self):
        """检查游戏是否结束
        
        Returns:
            bool: 游戏是否结束
        """
        # 游戏结束条件：任一玩家手牌为空
        return any(len(player.hand_cards) == 0 for player in self.players.values())

    def _set_game_over(self):
        """设置游戏结束状态"""
        self.state = CEnvState.GAME_OVER
        self.current_player = None
        self.last_play_cards = {'role': None, 'cards': []}

    def _update_hand_cards(self, player_role: CRole, played_cards: list):
        """更新玩家手牌，移除玩家出的牌
        
        Args:
            player_role: 出牌玩家的角色
            played_cards: 玩家出的牌列表
        """
        player = self.players[player_role]
        for card in played_cards:
            if card in player.hand_cards:
                player.hand_cards.remove(card)
            else:
                raise ValueError(f"玩家 {player_role} 的手牌中没有 {card}，无法移除")

    def _next_player(self, current_player: CRole) -> CRole:
        """根据当前玩家角色返回下一个玩家角色
        
        Args:
            current_player: 当前玩家的角色
            
        Returns:
            CRole: 下一个玩家的角色
        """
        if current_player == CRole.LANDLORD:
            return CRole.LANDLORD_UP
        elif current_player == CRole.LANDLORD_UP:
            return CRole.LANDLORD_DOWN
        elif current_player == CRole.LANDLORD_DOWN:
            return CRole.LANDLORD
        else:
            raise ValueError(f"未知的玩家角色: {current_player}")