class CRecord:
    def __init__(self, three_landlord_cards):
        # num_cards_left_dicts
        self.num_cards_left_dicts = {
            'landlord': 20,
            'landlord_up': 17,
            'landlord_down': 17
        }

        # # other_hand_cards
        # self.other_hand_cards = {
        #     'landlord': [],
        #     'landlord_up': [],
        #     'landlord_down': []
        # }

        # played_cards
        self.played_cards = {
            'landlord': [],
            'landlord_up': [],
            'landlord_down': []
        }

        # three_landlord_cards
        self.three_landlord_cards = three_landlord_cards

        # card_play_action_seq
        self.card_play_action_seq = []

        self.last_played_cards = {
            'role': None,
            'cards': []
        }

        self.play_card_seq = []  # 记录每一步的出牌行为，格式可以是一个列表，每个元素包含玩家角色和出牌内容等信息

    def update(self, player_role, played_cards):
        """更新游戏记录，记录玩家的出牌行为
        
        Args:
        
            player_role: 出牌玩家的角色
            played_cards: 玩家出的牌列表
            
        Returns:
            更新后的游戏记录
        """
        # 这里可以根据实际需求设计游戏记录的结构和更新逻辑
        # 例如，可以记录每一步的玩家角色和出牌内容
        self.played_cards[player_role].extend(played_cards)  # 更新玩家的出牌记录
        self.card_play_action_seq.append(played_cards)  # 记录玩家的出牌动作序列
        self.num_cards_left_dicts[player_role] -= len(played_cards)  # 更新玩家剩余牌数
        self.last_played_cards = {
            'role': player_role,
            'cards': played_cards
        }  # 更新上次出牌记录
        self.play_card_seq.append(played_cards)  # 记录每一步的出牌行为