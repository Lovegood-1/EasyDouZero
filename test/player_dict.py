"""
单元测试：CPlayerDict 玩家字典数据结构
"""
import unittest
import sys
sys.path.insert(0, '/home/yinzp/files/code/EasyDouZero')

from src.base_element.PlayerDict import CPlayerDict
from src.base_element.Role import CRole
from src.player.RandomPlayer import RandomPlayer


class TestCPlayerDict(unittest.TestCase):
    """测试 CPlayerDict 类"""
    
    def setUp(self):
        """每个测试前的准备工作"""
        self.player1 = RandomPlayer()
        self.player2 = RandomPlayer()
        self.player3 = RandomPlayer()
    
    def test_init_with_all_three_roles(self):
        """测试：正确初始化包含所有三个角色"""
        players = CPlayerDict({
            CRole.LANDLORD: self.player1,
            CRole.LANDLORD_UP: self.player2,
            CRole.LANDLORD_DOWN: self.player3
        })
        
        self.assertIsNotNone(players)
        self.assertEqual(len(players), 3)
    
    def test_init_missing_role_raises_error(self):
        """测试：缺少角色时抛出 ValueError"""
        with self.assertRaises(ValueError) as context:
            CPlayerDict({
                CRole.LANDLORD: self.player1,
                CRole.LANDLORD_UP: self.player2
                # 缺少 LANDLORD_DOWN
            })
        
        self.assertIn("缺少必需的角色", str(context.exception))
    
    def test_getitem(self):
        """测试：通过角色获取玩家"""
        players = CPlayerDict({
            CRole.LANDLORD: self.player1,
            CRole.LANDLORD_UP: self.player2,
            CRole.LANDLORD_DOWN: self.player3
        })
        
        self.assertEqual(players[CRole.LANDLORD], self.player1)
        self.assertEqual(players[CRole.LANDLORD_UP], self.player2)
        self.assertEqual(players[CRole.LANDLORD_DOWN], self.player3)
    
    def test_setitem(self):
        """测试：修改角色对应的玩家"""
        players = CPlayerDict({
            CRole.LANDLORD: self.player1,
            CRole.LANDLORD_UP: self.player2,
            CRole.LANDLORD_DOWN: self.player3
        })
        
        new_player = RandomPlayer()
        players[CRole.LANDLORD] = new_player
        
        self.assertEqual(players[CRole.LANDLORD], new_player)
    
    def test_iter(self):
        """测试：迭代所有角色"""
        players = CPlayerDict({
            CRole.LANDLORD: self.player1,
            CRole.LANDLORD_UP: self.player2,
            CRole.LANDLORD_DOWN: self.player3
        })
        
        roles = set(players)
        expected_roles = {CRole.LANDLORD, CRole.LANDLORD_UP, CRole.LANDLORD_DOWN}
        
        self.assertEqual(roles, expected_roles)
    
    def test_contains(self):
        """测试：判断角色是否存在"""
        players = CPlayerDict({
            CRole.LANDLORD: self.player1,
            CRole.LANDLORD_UP: self.player2,
            CRole.LANDLORD_DOWN: self.player3
        })
        
        self.assertIn(CRole.LANDLORD, players)
        self.assertIn(CRole.LANDLORD_UP, players)
        self.assertIn(CRole.LANDLORD_DOWN, players)
    
    def test_access_all_roles(self):
        """测试：确保所有三个角色都可以访问"""
        players = CPlayerDict({
            CRole.LANDLORD: self.player1,
            CRole.LANDLORD_UP: self.player2,
            CRole.LANDLORD_DOWN: self.player3
        })
        
        # 验证每个角色都能正确访问
        self.assertIsInstance(players[CRole.LANDLORD], RandomPlayer)
        self.assertIsInstance(players[CRole.LANDLORD_UP], RandomPlayer)
        self.assertIsInstance(players[CRole.LANDLORD_DOWN], RandomPlayer)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
