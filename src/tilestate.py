from enum import Enum

class TileState(Enum):
    IDLE = (0, 0, 0)
    HOVER = (128, 128, 128)
    ACTIVE = (0, 255, 0)
