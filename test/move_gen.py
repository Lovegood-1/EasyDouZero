
from pathlib import Path
import sys

 
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.Env import CEnv
from src.base_element.GameMode import CGameMode
from src.base_element.Role import CRole
from src.player.RandomPlayer import RandomPlayer
from src.move.generate import CGenerate, gen_moves_by_hand_cards_and_trival
 
def test_move_generation():
    """测试 move generation 的基本功能"""
    print("\n=== 测试 move generation ===")
    
    
    # 这里可以添加更多关于 move generation 的测试逻辑，例如验证生成的 moves 是否符合预期
    gen = CGenerate(cards_list=[4,4,4,4])
    print(f"生成的单牌 moves: {gen.gen_type_4_bomb()}")  # 示例输出炸弹组合

def test_generate_move_by_hand_cards_and_trival():
    hand_cards = [3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
    trival_cards = [3, 3, 4, 4, 5, 5,]
    gen = gen_moves_by_hand_cards_and_trival(hand_cards=hand_cards, rival_cards=trival_cards)
    expected = [
        [4, 4, 5, 5, 6, 6],
        [5, 5, 6, 6, 7, 7],
        [6, 6, 7, 7, 8, 8],
        [7, 7, 8, 8, 9, 9],
        []
    ]
    assert gen == expected, f"gen 不符合预期，实际: {gen}, 期望: {expected}"
    print(f"根据手牌和三张牌生成的 moves: {gen}")

def test_generate_move_by_hand_cards_and_trival2():
    hand_cards = [3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
    trival_cards = []
    gen = gen_moves_by_hand_cards_and_trival(hand_cards=hand_cards, rival_cards=trival_cards)
 
    print(f"根据手牌和三张牌生成的 moves: {gen}")

# 无牌可出，需要返回 []，而不是 None 或其他值
def test_generate_move_by_hand_cards_and_trival3():
    hand_cards = [3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
    trival_cards = [9, 9, 9]  # 这里的三张牌是玩家手牌中最大的牌，理论上应该没有牌能打过它
    gen = gen_moves_by_hand_cards_and_trival(hand_cards=hand_cards, rival_cards=trival_cards)
 
    print(f"根据手牌和三张牌生成的 moves: {gen}")

if __name__ == '__main__':
    test_move_generation()
    test_generate_move_by_hand_cards_and_trival()
    test_generate_move_by_hand_cards_and_trival2()
    test_generate_move_by_hand_cards_and_trival3()
    print('test_main_env passed')