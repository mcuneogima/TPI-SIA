from pathlib import Path

from .estado import Estado
from .mapa import Mapa, Posicion


SIMBOLOS_VALIDOS = {"#", " ", ".", "$", "@", "*", "+"}


def cargar_nivel(ruta: str | Path) -> Estado:
    ruta = Path(ruta)
    texto = ruta.read_text(encoding="utf-8")
    return parsear_nivel(texto)


def parsear_nivel(texto: str) -> Estado:
    lineas = texto.splitlines()

    while lineas and lineas[-1] == "":
        lineas.pop()

    if not lineas:
        raise ValueError("El nivel está vacío.")

    ancho = len(lineas[0])
    if ancho == 0:
        raise ValueError("El nivel contiene una fila vacía.")

    if any(len(linea) != ancho for linea in lineas):
        raise ValueError("Todas las filas del nivel deben tener el mismo ancho.")

    paredes: set[Posicion] = set()
    objetivos: set[Posicion] = set()
    cajas: set[Posicion] = set()
    jugador: Posicion | None = None

    for fila, linea in enumerate(lineas):
        for columna, simbolo in enumerate(linea):
            if simbolo not in SIMBOLOS_VALIDOS:
                raise ValueError(
                    f"Símbolo inválido {simbolo!r} en ({fila}, {columna})."
                )

            posicion = (fila, columna)

            if simbolo == "#":
                paredes.add(posicion)
            elif simbolo == ".":
                objetivos.add(posicion)
            elif simbolo == "$":
                cajas.add(posicion)
            elif simbolo == "@":
                if jugador is not None:
                    raise ValueError("El nivel tiene más de un jugador.")
                jugador = posicion
            elif simbolo == "*":
                cajas.add(posicion)
                objetivos.add(posicion)
            elif simbolo == "+":
                if jugador is not None:
                    raise ValueError("El nivel tiene más de un jugador.")
                jugador = posicion
                objetivos.add(posicion)

    if jugador is None:
        raise ValueError("El nivel no tiene jugador (@ o +).")

    mapa = Mapa(
        alto=len(lineas),
        ancho=ancho,
        paredes=frozenset(paredes),
        objetivos=frozenset(objetivos),
    )
    return Estado(mapa, jugador, frozenset(cajas))
