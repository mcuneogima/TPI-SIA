from collections.abc import Callable

from src.modelos.estado import Estado
from .manhattan import manhattan
from .paredes_bfs import crear_paredes_bfs


def obtener_heuristica(nombre: str, estado_inicial: Estado) -> Callable[[Estado], float]:
    normalizado = nombre.strip().lower()

    if normalizado in {"manhattan", "m"}:
        return manhattan

    if normalizado in {"paredes_bfs", "paredes", "push", "push_bfs"}:
        return crear_paredes_bfs(estado_inicial)

    raise ValueError(
        f"Heurística desconocida: {nombre}. "
        "Opciones: manhattan, paredes_bfs."
    )
