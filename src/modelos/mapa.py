from dataclasses import dataclass
from typing import FrozenSet


Posicion = tuple[int, int]


@dataclass(frozen=True, slots=True)
class Mapa:
    alto: int
    ancho: int
    paredes: FrozenSet[Posicion]
    objetivos: FrozenSet[Posicion]

    def dentro(self, posicion: Posicion) -> bool:
        fila, columna = posicion
        return 0 <= fila < self.alto and 0 <= columna < self.ancho

    def transitable(self, posicion: Posicion) -> bool:
        return self.dentro(posicion) and posicion not in self.paredes
