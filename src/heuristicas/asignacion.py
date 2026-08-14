from functools import lru_cache
from math import inf


def costo_emparejamiento(matriz: list[list[float]]) -> float:
    """Costo mínimo de asignar cada fila a un objetivo distinto.

    Usa programación dinámica sobre subconjuntos. Devuelve infinito si no
    existe un emparejamiento finito.
    """
    n = len(matriz)
    if n == 0:
        return 0.0

    @lru_cache(maxsize=None)
    def dp(fila: int, usados: int) -> float:
        if fila == n:
            return 0.0

        mejor = inf
        for columna, costo in enumerate(matriz[fila]):
            if usados & (1 << columna):
                continue
            if costo == inf:
                continue

            restante = dp(fila + 1, usados | (1 << columna))
            if restante != inf:
                mejor = min(mejor, costo + restante)

        return mejor

    return dp(0, 0)
