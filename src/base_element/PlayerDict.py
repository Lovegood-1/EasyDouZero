from src.base_element.Role import CRole
from typing import Dict
from src.base_element.Agent import CAgent

class CPlayer:
    # hand_cards: list
    # angent: CAgent
    def __init__(self, agent: CAgent):
        self.hand_cards = []
        self.agent = agent  # 这里可以根据实际需求设置默认的 agent，例如一个随机 agent 或者一个简单的规则 agent

class CPlayerDict:
    """玩家字典数据结构，强制要求必须包含三个固定角色的玩家
    
    必须包含的角色：地主(LANDLORD)、地主上家(LANDLORD_UP)、地主下家(LANDLORD_DOWN)
    """
    
    def __init__(self, players: Dict[CRole, CPlayer]):
        """初始化玩家字典
        
        Args:
            players: 角色到玩家的映射字典，必须包含三个角色
            
        Raises:
            ValueError: 如果缺少必需的角色
        """
        required_roles = {CRole.LANDLORD, CRole.LANDLORD_UP, CRole.LANDLORD_DOWN}
        provided_roles = set(players.keys())
        
        # 检查是否包含所有必需的角色
        missing_roles = required_roles - provided_roles
        if missing_roles:
            raise ValueError(f"缺少必需的角色: {missing_roles}")
        
        # 检查是否有多余的角色
        extra_roles = provided_roles - required_roles
        if extra_roles:
            raise ValueError(f"包含了无效的角色: {extra_roles}")
        
        self._players = players
    
    def __getitem__(self, role: CRole) -> CPlayer:
        """通过角色获取玩家对象"""
        return self._players[role]
    
    def __setitem__(self, role: CRole, player: CPlayer):
        """设置角色对应的玩家对象"""
        if role not in [CRole.LANDLORD, CRole.LANDLORD_UP, CRole.LANDLORD_DOWN]:
            raise KeyError(f"只能设置这三个角色: LANDLORD, LANDLORD_UP, LANDLORD_DOWN")
        self._players[role] = player
    
    def __iter__(self):
        """迭代所有角色"""
        return iter(self._players)

    def __len__(self):
        """返回玩家字典中角色的数量"""
        return len(self._players)
    