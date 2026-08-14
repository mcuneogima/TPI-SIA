from dataclasses import dataclass
from typing import Callable

from src.modelos.accion import Accion
from src.modelos.estado import Estado
from src.modelos.movimiento import aplicar_accion

Heuristica = Callable[[Estado], float]

ORDEN_ACCIONES = (
    Accion.UP,
    Accion.RIGHT,
    Accion.DOWN,
    Accion.LEFT,
)


@dataclass(slots=True)
class Nodo:
    estado: Estado
    padre: "Nodo | None"
    accion: Accion | None
    costo: int
    profundidad: int

    def camino(self) -> list[Accion]:
        acciones: list[Accion] = []
        nodo: Nodo | None = self

        while nodo is not None and nodo.accion is not None:
            acciones.append(nodo.accion)
            nodo = nodo.padre

        acciones.reverse()
        return acciones


@dataclass(slots=True)
class ResultadoBusqueda:
    success: bool
    costo: int | None
    nodos_expandidos: int
    nodos_frontal: int
    acciones: list[Accion]
    nodo_final: Nodo | None

    @property
    def solution_length(self) -> int:
        return len(self.acciones)


def sucesores(nodo: Nodo):
    for accion in ORDEN_ACCIONES:
        nuevo_estado = aplicar_accion(nodo.estado, accion)
        if nuevo_estado is not None:
            yield accion, nuevo_estado
