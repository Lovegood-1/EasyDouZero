"""
测试 CEnv 状态机功能
验证状态转换和异常处理
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.Env import CEnv
from src.base_element.GameMode import CGameMode
from src.base_element.EnvState import CEnvState
from src.base_element.Role import CRole
from src.player.RandomPlayer import RandomPlayer


def build_players():
    return {
        CRole.LANDLORD: RandomPlayer(),
        CRole.LANDLORD_UP: RandomPlayer(),
        CRole.LANDLORD_DOWN: RandomPlayer(),
    }


def test_normal_flow():
    """测试正常流程：创建 → start → step → end"""
    print("\n=== 测试正常流程 ===")
    game = CEnv(mode=CGameMode.SANDBOX, players=build_players())
    
    # 初始状态应为 IDLE
    assert game.state == CEnvState.IDLE
    assert game.step_count is None
    print("✓ 初始状态：IDLE")
    
    # 开始游戏
    game.play_start()
    assert game.state == CEnvState.PLAYING
    assert game.step_count == 0
    print("✓ 调用 play_start() 后状态：PLAYING")
    
    # 执行步骤
    step_count = 0
    while not game.play_end():
        game.play_step()
        step_count += 1
    
    assert game.state == CEnvState.GAME_OVER
    assert step_count == 10
    print(f"✓ 执行 {step_count} 步后状态：GAME_OVER")


def test_step_before_start():
    """测试异常情况：未调用 play_start() 直接调用 play_step()"""
    print("\n=== 测试异常：未 start 直接 step ===")
    game = CEnv(mode=CGameMode.SANDBOX, players=build_players())
    
    try:
        game.play_step()
        assert False, "应该抛出 RuntimeError"
    except RuntimeError as e:
        print(f"✓ 正确抛出异常：{e}")
        assert "IDLE" in str(e)


def test_step_after_game_over():
    """测试异常情况：游戏结束后继续调用 play_step()"""
    print("\n=== 测试异常：游戏结束后调用 step ===")
    game = CEnv(mode=CGameMode.SANDBOX, players=build_players())
    game.play_start()
    
    # 执行到游戏结束
    while not game.play_end():
        game.play_step()
    
    assert game.state == CEnvState.GAME_OVER
    
    # 尝试在游戏结束后继续 step
    try:
        game.play_step()
        assert False, "应该抛出 RuntimeError"
    except RuntimeError as e:
        print(f"✓ 正确抛出异常：{e}")
        assert "GAME_OVER" in str(e)


def test_multiple_start():
    """测试异常情况：多次调用 play_start()"""
    print("\n=== 测试异常：多次调用 start ===")
    game = CEnv(mode=CGameMode.SANDBOX, players=build_players())
    game.play_start()
    
    assert game.state == CEnvState.PLAYING
    
    # 尝试再次 start
    try:
        game.play_start()
        assert False, "应该抛出 RuntimeError"
    except RuntimeError as e:
        print(f"✓ 正确抛出异常：{e}")
        assert "PLAYING" in str(e)


def test_end_flag_removed():
    """验证 end_flag 属性已被移除"""
    print("\n=== 测试：end_flag 已移除 ===")
    game = CEnv(mode=CGameMode.SANDBOX, players=build_players())
    
    assert not hasattr(game, 'end_flag')
    print("✓ end_flag 属性已被移除")


if __name__ == '__main__':
    test_normal_flow()
    test_step_before_start()
    test_step_after_game_over()
    test_multiple_start()
    test_end_flag_removed()
    print("\n" + "="*50)
    print("所有测试通过！✅")
    print("="*50)
