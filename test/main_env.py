
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.Env import CEnv
from src.base_element.GameMode import CGameMode
from src.base_element.Role import CRole
from src.player.RandomPlayer import RandomPlayer


def build_players():
    return {
        CRole.LANDLORD: RandomPlayer(),
        CRole.LANDLORD_UP: RandomPlayer(),
        CRole.LANDLORD_DOWN: RandomPlayer(),
    }


def test_env_init():
    players = build_players()
    game = CEnv(mode=CGameMode.SANDBOX, players=players)

    assert game.mode == CGameMode.SANDBOX
    assert game.players == players
    assert len(game.players) == 3
    assert all(isinstance(player, RandomPlayer) for player in game.players.values())

# 一般流程
def test_env_pipeline():
    game = CEnv(mode=CGameMode.SANDBOX, players=build_players())
    game.start() # 发牌等初始化步骤
    while not game.end():
        # 打印是谁需要出牌，上次出牌是什么，这次可以出的牌是什么
        # 打印当前所有玩家的手牌和身份
        for role, player in game.players.items():
            print(f"玩家 {role} 的手牌: {player.hand_cards}")
        actions = game.cur_legal_actions()
        action = actions[-1]
        print(f"当前玩家: {game.current_player}, 上次出牌: {game.last_play_cards}, 可出牌: {actions}")
        print(f"默认选择第一种可出的牌进行出牌：{action}")
        game.step(action)

# 开始阶段：测试 start() 方法是否正确初始化游戏状态（发牌和身份）
def test_env_start():
    game = CEnv(mode=CGameMode.SANDBOX, players=build_players())
    game.start()
    # 打印玩家手牌和身份, 检查手牌的数量
    for role, player in game.players.items():
        if role == CRole.LANDLORD:
            assert len(player.hand_cards) == 20  # 地主应该有 20 张牌
        else:
            assert len(player.hand_cards) == 17  # 农民应该有 17 张牌
    # 检查底牌
    assert len(game.three_landlord_cards) == 3  # 底牌应该有 3 张


if __name__ == '__main__':
    test_env_init()
    test_env_pipeline()
    test_env_start()
    print('test_main_env passed')