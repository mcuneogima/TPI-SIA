import heapq
from itertools import count

from .base import Heuristica, Nodo, ResultadoBusqueda, sucesores


def greedy(inicial, heuristica: Heuristica) -> ResultadoBusqueda:
    contador = count()
    raiz = Nodo(inicial, None, None, 0, 0)

    frontera = [(heuristica(inicial), next(contador), raiz)]
    visitados = {inicial.clave()}
    expandidos = 0

    while frontera:
        _, _, nodo = heapq.heappop(frontera)

        if nodo.estado.es_objetivo():
            return ResultadoBusqueda(
                True,
                nodo.costo,
                expandidos,
                len(frontera),
                nodo.camino(),
                nodo,
            )

        expandidos += 1

        for accion, estado in sucesores(nodo):
            clave = estado.clave()
            if clave in visitados:
                continue

            hijo = Nodo(
                estado,
                nodo,
                accion,
                nodo.costo + 1,
                nodo.profundidad + 1,
            )
            visitados.add(clave)
            heapq.heappush(
                frontera,
                (heuristica(estado), next(contador), hijo),
            )

    return ResultadoBusqueda(False, None, expandidos, 0, [], None)
