
from src.game.GameEnv import CGameEnv
from src.base_element.GameMode import CGameMode
from src.base_element.Role import CRole
from src.player.RandomPlayer import RandomPlayer

dictPlayers = {
    CRole.LANDLORD: RandomPlayer(),
    CRole.LANDLORD_UP: RandomPlayer(),
    CRole.LANDLORD_DOWN: RandomPlayer()
}
game = CGameEnv(mode=CGameMode.SANDBOX, players=dictPlayers)