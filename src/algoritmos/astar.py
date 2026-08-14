import heapq
from itertools import count

from .base import Heuristica, Nodo, ResultadoBusqueda, sucesores


def astar(inicial, heuristica: Heuristica) -> ResultadoBusqueda:
    contador = count()
    raiz = Nodo(inicial, None, None, 0, 0)

    frontera = [(heuristica(inicial), next(contador), raiz)]
    mejor_g = {inicial.clave(): 0}
    expandidos = 0

    while frontera:
        _, _, nodo = heapq.heappop(frontera)
        clave_nodo = nodo.estado.clave()

        if nodo.costo != mejor_g.get(clave_nodo):
            continue

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
            nuevo_g = nodo.costo + 1
            clave = estado.clave()

            if nuevo_g >= mejor_g.get(clave, float("inf")):
                continue

            hijo = Nodo(
                estado,
                nodo,
                accion,
                nuevo_g,
                nodo.profundidad + 1,
            )
            mejor_g[clave] = nuevo_g
            f = nuevo_g + heuristica(estado)
            heapq.heappush(frontera, (f, next(contador), hijo))

    return ResultadoBusqueda(False, None, expandidos, 0, [], None)
