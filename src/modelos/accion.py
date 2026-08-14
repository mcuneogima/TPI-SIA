from enum import Enum


class Accion(str, Enum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"

    @property
    def delta(self) -> tuple[int, int]:
        return {
            Accion.UP: (-1, 0),
            Accion.RIGHT: (0, 1),
            Accion.DOWN: (1, 0),
            Accion.LEFT: (0, -1),
        }[self]
