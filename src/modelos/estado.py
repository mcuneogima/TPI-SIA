from dataclasses import dataclass
from typing import FrozenSet

from .mapa import Mapa, Posicion


@dataclass(frozen=True, slots=True)
class Estado:
    mapa: Mapa
    jugador: Posicion
    cajas: FrozenSet[Posicion]

    def es_objetivo(self) -> bool:
        return self.cajas.issubset(self.mapa.objetivos)

    def clave(self) -> tuple[Posicion, FrozenSet[Posicion]]:
        # El mapa es fijo durante una ejecución, por lo que no hace falta
        # incluirlo en la clave lógica del estado.
        return self.jugador, self.cajas
