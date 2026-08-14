from dataclasses import asdict, dataclass
from typing import Any

from src.modelos.accion import Accion
from src.algoritmos.base import ResultadoBusqueda


@dataclass(slots=True)
class ResultadoEjecucion:
    level: str
    algorithm: str
    heuristic: str
    success: bool
    cost: int | None
    nodes_expanded: int
    nodes_frontier: int
    time_ms: float
    memory_mb: float
    solution: str
    solution_length: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def construir_resultado(
    *,
    level: str,
    algorithm: str,
    heuristic: str,
    busqueda: ResultadoBusqueda,
    time_ms: float,
    memory_mb: float,
) -> ResultadoEjecucion:
    solucion = " ".join(accion.value for accion in busqueda.acciones)

    return ResultadoEjecucion(
        level=level,
        algorithm=algorithm,
        heuristic=heuristic,
        success=busqueda.success,
        cost=busqueda.costo,
        nodes_expanded=busqueda.nodos_expandidos,
        nodes_frontier=busqueda.nodos_frontal,
        time_ms=round(time_ms, 3),
        memory_mb=round(memory_mb, 3),
        solution=solucion,
        solution_length=busqueda.solution_length,
    )
