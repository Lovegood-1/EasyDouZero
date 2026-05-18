
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
from src.agent.DeepLordAgent import CDeepLordAgent
from src.agent.DeepFramerAgent import CDeepFramerAgent
from src.model.FamerModel import CFarmerLstmModel
from src.model.LandlordModel import CLandlordLstmModel

def build_random_players():
    return {
        CRole.LANDLORD: CPlayer(CSmallAgent()),
        CRole.LANDLORD_UP: CPlayer(CSmallAgent()),
        CRole.LANDLORD_DOWN: CPlayer(CLargeAgent()),
    }

def build_deep_lord_players():
    return {
        CRole.LANDLORD: CPlayer(CDeepLordAgent(CRole.LANDLORD, model=CLandlordLstmModel())),
        CRole.LANDLORD_UP: CPlayer(CDeepFramerAgent(CRole.LANDLORD_UP, model=CFarmerLstmModel())),
        CRole.LANDLORD_DOWN: CPlayer(CDeepFramerAgent(CRole.LANDLORD_DOWN, model=CFarmerLstmModel())),
    }

def test_agent_pipeline():
    game = CEnv(mode=CGameMode.SANDBOX, players=build_random_players())
    game.play_start() # 发牌等初始化步骤
    while not game.play_end():
        for role, player in game.players.items():
            print(f"玩家 {role} 的手牌: {player.hand_cards}")
        # 打印 game records
        print(f"游戏记录: {game.record}")
        actions = game.cur_legal_actions()
        action = game.players[game.current_player].agent.select_action(actions)  # 这里假设玩家对象有一个 agent 属性，agent 有一个 select_action 方法
        print(f"当前玩家: {game.current_player}, 出牌: {action}")
        game.play_step(action)

def test_deep_agent_pipeline():
    game = CEnv(mode=CGameMode.SANDBOX, players=build_deep_lord_players())
    game.play_start() # 发牌等初始化步骤
    while not game.play_end():
        for role, player in game.players.items():
            print(f"玩家 {role} 的手牌: {player.hand_cards}")
        # 打印 game records
        print(f"游戏记录: {game.record}")
        actions = game.cur_legal_actions()
        action = game.players[game.current_player].agent.select_action(game.players[game.current_player], actions, game.record)  # 这里假设玩家对象有一个 agent 属性，agent 有一个 select_action 方法
        print(f"当前玩家: {game.current_player}, 出牌: {action}")
        game.play_step(action)

if __name__ == '__main__':
    test_agent_pipeline()
    test_deep_agent_pipeline()
    print('test_main_env passed')