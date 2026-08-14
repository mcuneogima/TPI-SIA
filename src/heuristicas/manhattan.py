from math import inf

from src.modelos.estado import Estado
from .asignacion import costo_emparejamiento


def manhattan(estado: Estado) -> float:
    """Distancia Manhattan mínima entre cajas y objetivos."""
    cajas = list(estado.cajas)
    objetivos = list(estado.mapa.objetivos)

    matriz = [
        [
            abs(caja[0] - objetivo[0]) + abs(caja[1] - objetivo[1])
            for objetivo in objetivos
        ]
        for caja in cajas
    ]

    valor = costo_emparejamiento(matriz)
    return valor if valor != inf else inf
