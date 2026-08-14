from collections import deque
from math import inf

from src.modelos.estado import Estado, Posicion
from .asignacion import costo_emparejamiento


def _distancias_desde_objetivo(estado: Estado, objetivo: Posicion) -> dict[Posicion, int]:
    """Distancia mínima de empuje desde cada posición de caja al objetivo.

    Es un BFS inverso: si una caja podría ser empujada desde `anterior` hacia
    `actual`, el jugador tendría que estar en `anterior - direccion`.
    Solo se consideran paredes; cajas y posición actual del jugador se ignoran.
    """
    mapa = estado.mapa
    distancias = {objetivo: 0}
    cola = deque([objetivo])

    while cola:
        actual = cola.popleft()
        distancia = distancias[actual]

        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            anterior = (actual[0] - dr, actual[1] - dc)
            posicion_jugador = (anterior[0] - dr, anterior[1] - dc)

            if not mapa.transitable(anterior):
                continue
            if not mapa.transitable(posicion_jugador):
                continue
            if anterior in distancias:
                continue

            distancias[anterior] = distancia + 1
            cola.append(anterior)

    return distancias


def paredes_bfs(estado: Estado) -> float:
    """Mínimo número de empujes ignorando otras cajas y al jugador."""
    objetivos = list(estado.mapa.objetivos)
    tablas = {
        objetivo: _distancias_desde_objetivo(estado, objetivo)
        for objetivo in objetivos
    }

    matriz = [
        [tablas[objetivo].get(caja, inf) for objetivo in objetivos]
        for caja in estado.cajas
    ]

    return costo_emparejamiento(matriz)


def crear_paredes_bfs(estado_inicial: Estado):
    """Crea una heurística con las distancias estáticas precalculadas.

    Esto evita repetir BFS en cada nodo de búsqueda.
    """
    objetivos = list(estado_inicial.mapa.objetivos)
    tablas = {
        objetivo: _distancias_desde_objetivo(estado_inicial, objetivo)
        for objetivo in objetivos
    }

    def heuristica(estado: Estado) -> float:
        matriz = [
            [tablas[objetivo].get(caja, inf) for objetivo in objetivos]
            for caja in estado.cajas
        ]
        return costo_emparejamiento(matriz)

    return heuristica
