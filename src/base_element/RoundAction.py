from enum import Enum, auto


class CRoundAction(Enum):
    PASS  = auto()
    CALL  = auto()
    RAISE = auto()