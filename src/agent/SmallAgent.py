from src.base_element.Agent import CAgent

class CSmallAgent(CAgent):

    def __init__(self):
        super().__init__()
        self.name = 'SmallAgent'

    def select_action(self, legal_actions):
        return legal_actions[0]
