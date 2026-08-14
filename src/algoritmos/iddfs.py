from .base import Nodo, ResultadoBusqueda, ORDEN_ACCIONES
from src.modelos.movimiento import aplicar_accion


def iddfs(inicial, max_depth: int | None = None) -> ResultadoBusqueda:
    """Iterative Deepening DFS sobre el costo en movimientos.

    Cada iteración explora profundidades 0, 1, 2, ... hasta encontrar una
    solución o alcanzar max_depth.
    """
    if inicial.es_objetivo():
        return ResultadoBusqueda(True, 0, 0, 0, [], Nodo(inicial, None, None, 0, 0))

    limite = 0
    total_expandidos = 0

    while max_depth is None or limite <= max_depth:
        resultado, expandidos = _dls(inicial, limite)
        total_expandidos += expandidos

        if resultado is not None:
            resultado.nodos_expandidos = total_expandidos
            return resultado

        limite += 1

    return ResultadoBusqueda(False, None, total_expandidos, 0, [], None)


def _dls(inicial, limite: int):
    raiz = Nodo(inicial, None, None, 0, 0)
    expandidos = 0
    # Guarda el menor límite restante con el que vimos una clave. Esto evita
    # ciclos inútiles sin eliminar caminos potencialmente útiles.
    mejor_restante = {inicial.clave(): limite}

    def visitar(nodo: Nodo, restante: int):
        nonlocal expandidos

        if nodo.estado.es_objetivo():
            return ResultadoBusqueda(
                True,
                nodo.costo,
                expandidos,
                0,
                nodo.camino(),
                nodo,
            )

        if restante == 0:
            return None

        expandidos += 1

        for accion in ORDEN_ACCIONES:
            estado = aplicar_accion(nodo.estado, accion)
            if estado is None:
                continue

            clave = estado.clave()
            nuevo_restante = restante - 1

            # Si ya llegamos al mismo estado con igual o mayor profundidad
            # restante, continuar no aporta nada en esta iteración.
            if nuevo_restante <= mejor_restante.get(clave, -1):
                continue

            mejor_restante[clave] = nuevo_restante

            hijo = Nodo(
                estado,
                nodo,
                accion,
                nodo.costo + 1,
                nodo.profundidad + 1,
            )
            resultado = visitar(hijo, nuevo_restante)

            if resultado is not None:
                return resultado

        return None

    return visitar(raiz, limite), expandidos
