from .base import Nodo, ResultadoBusqueda, ORDEN_ACCIONES
from src.modelos.movimiento import aplicar_accion


def dfs(inicial) -> ResultadoBusqueda:
    raiz = Nodo(inicial, None, None, 0, 0)
    if inicial.es_objetivo():
        return ResultadoBusqueda(True, 0, 0, 0, [], raiz)

    frontera = [raiz]
    visitados = {inicial.clave()}
    expandidos = 0

    while frontera:
        nodo = frontera.pop()
        expandidos += 1

        # Se agregan en orden inverso para que el primero explorado sea UP.
        sucesores = []
        for accion in ORDEN_ACCIONES:
            nuevo_estado = aplicar_accion(nodo.estado, accion)

            if nuevo_estado is not None:
                sucesores.append((accion, nuevo_estado))

        for accion, estado in reversed(sucesores):
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
