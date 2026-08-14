from collections import deque

from .base import Nodo, ResultadoBusqueda, sucesores


def bfs(inicial) -> ResultadoBusqueda:
    raiz = Nodo(inicial, None, None, 0, 0)
    if inicial.es_objetivo():
        return ResultadoBusqueda(True, 0, 0, 0, [], raiz)

    frontera = deque([raiz])
    visitados = {inicial.clave()}
    expandidos = 0

    while frontera:
        nodo = frontera.popleft()
        expandidos += 1

        for accion, estado in sucesores(nodo):
            clave = estado.clave()
            if clave in visitados:
                continue

            hijo = Nodo(
                estado=estado,
                padre=nodo,
                accion=accion,
                costo=nodo.costo + 1,
                profundidad=nodo.profundidad + 1,
            )

            if estado.es_objetivo():
                return ResultadoBusqueda(
                    True,
                    hijo.costo,
                    expandidos,
                    len(frontera),
                    hijo.camino(),
                    hijo,
                )

            visitados.add(clave)
            frontera.append(hijo)

    return ResultadoBusqueda(False, None, expandidos, 0, [], None)
