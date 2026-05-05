from src.base_element.Record import CRecord

class CAgent:
    def __init__(self):
        pass

    def select_action(self, legal_actions, records: CRecord):
        """根据合法动作列表选择一个动作
        
        Args:
            legal_actions: 当前玩家的合法动作列表
            records: 游戏历史记录
            
        Returns:
            选择的动作，必须在 legal_actions 中
        """
        # 这里可以实现具体的策略，例如随机选择、基于规则的选择、基于模型的选择等
        # 目前默认返回第一个合法动作作为示例
        return legal_actions[0] if legal_actions else None
