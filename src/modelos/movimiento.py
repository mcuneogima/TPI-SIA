from .accion import Accion
from .estado import Estado
from .mapa import Posicion


def aplicar_accion(estado: Estado, accion: Accion) -> Estado | None:
    """Aplica una acción de Sokoban. Devuelve None si la acción es inválida.

    Una acción cuesta exactamente un movimiento, tanto al caminar como al
    empujar. Empujar es posible solamente si la celda inmediatamente posterior
    a la caja es transitable y no contiene otra caja.
    """
    dr, dc = accion.delta
    jugador = estado.jugador
    siguiente: Posicion = (jugador[0] + dr, jugador[1] + dc)

    if not estado.mapa.transitable(siguiente):
        return None

    if siguiente not in estado.cajas:
        return Estado(estado.mapa, siguiente, estado.cajas)

    # Hay una caja: el jugador intenta empujarla.
    destino_caja: Posicion = (siguiente[0] + dr, siguiente[1] + dc)

    if not estado.mapa.transitable(destino_caja):
        return None

    if destino_caja in estado.cajas:
        return None

    nuevas_cajas = set(estado.cajas)
    nuevas_cajas.remove(siguiente)
    nuevas_cajas.add(destino_caja)

    return Estado(estado.mapa, siguiente, frozenset(nuevas_cajas))
