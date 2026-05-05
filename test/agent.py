
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.Env import CEnv
from src.base_element.GameMode import CGameMode
from src.base_element.Role import CRole
from src.base_element.PlayerDict import CPlayer
from src.agent.SmallAgent import CSmallAgent
from src.agent.LargeAgent import CLargeAgent


def build_players():
    return {
        CRole.LANDLORD: CPlayer(CSmallAgent()),
        CRole.LANDLORD_UP: CPlayer(CSmallAgent()),
        CRole.LANDLORD_DOWN: CPlayer(CLargeAgent()),
    }

# 
def test_agent_pipeline():
    game = CEnv(mode=CGameMode.SANDBOX, players=build_players())
    game.start() # 发牌等初始化步骤
    while not game.end():
        for role, player in game.players.items():
            print(f"玩家 {role} 的手牌: {player.hand_cards}")
        # 打印 game records
        print(f"游戏记录: {game.record}")
        actions = game.cur_legal_actions()
        action = game.players[game.current_player].agent.select_action(actions, game.records, None)  # 这里假设玩家对象有一个 agent 属性，agent 有一个 select_action 方法
        print(f"当前玩家: {game.current_player}, 出牌: {action}")
        game.step(action)


if __name__ == '__main__':
    test_agent_pipeline()
    print('test_main_env passed')