from enum import Enum, auto

class CEnvState(Enum):
    """游戏环境状态枚举
    
    IDLE: 初始状态，游戏未开始
    PLAYING: 游戏进行中
    GAME_OVER: 游戏已结束
    """
    IDLE = auto()
    PLAYING = auto()
    GAME_OVER = auto()
