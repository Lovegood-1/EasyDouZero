from src.base_element.Agent import CAgent

class CLargeAgent(CAgent):

    def __init__(self):
        super().__init__()
        self.name = 'LargeAgent'

    def select_action(self, legal_actions):
        # Prefer the second-to-last action if possible, otherwise the last one
        if len(legal_actions) >= 2:
            return legal_actions[-2]
        return legal_actions[-1]
