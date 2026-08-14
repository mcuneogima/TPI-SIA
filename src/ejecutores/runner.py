import csv
import time
import tracemalloc
from pathlib import Path

from src.algoritmos.astar import astar
from src.algoritmos.bfs import bfs
from src.algoritmos.dfs import dfs
from src.algoritmos.greedy import greedy
from src.algoritmos.iddfs import iddfs
from src.heuristicas import obtener_heuristica
from src.modelos.parser import cargar_nivel
from src.resultados.resultado import ResultadoEjecucion, construir_resultado


ALGORITMOS = {
    "bfs": bfs,
    "dfs": dfs,
    "greedy": greedy,
    "astar": astar,
    "a*": astar,
    "iddfs": iddfs,
}

ALGORITMOS_CON_HEURISTICA = {"greedy", "astar", "a*"}

CAMPOS_CSV = [
    "level",
    "algorithm",
    "heuristic",
    "success",
    "cost",
    "nodes_expanded",
    "nodes_frontier",
    "time_ms",
    "memory_mb",
    "solution",
    "solution_length",
]


def ejecutar(
    nivel: str | Path,
    algoritmo: str,
    heuristica: str | None = None,
    *,
    max_depth: int | None = None,
) -> ResultadoEjecucion:
    nivel = Path(nivel)
    nombre_algoritmo = algoritmo.strip().lower()

    if nombre_algoritmo not in ALGORITMOS:
        raise ValueError(
            f"Algoritmo desconocido: {algoritmo}. "
            "Opciones: bfs, dfs, greedy, astar, iddfs."
        )

    if nombre_algoritmo in ALGORITMOS_CON_HEURISTICA and not heuristica:
        raise ValueError(
            f"{algoritmo} necesita una heurística: manhattan o paredes_bfs."
        )

    estado_inicial = cargar_nivel(nivel)
    busqueda = None

    tracemalloc.start()
    inicio = time.perf_counter_ns()

    try:
        funcion = ALGORITMOS[nombre_algoritmo]

        if nombre_algoritmo in ALGORITMOS_CON_HEURISTICA:
            h = obtener_heuristica(heuristica, estado_inicial)
            busqueda = funcion(estado_inicial, h)
        elif nombre_algoritmo == "iddfs":
            busqueda = funcion(estado_inicial, max_depth=max_depth)
        else:
            busqueda = funcion(estado_inicial)
    finally:
        tiempo_ms = (time.perf_counter_ns() - inicio) / 1_000_000
        _, memoria_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    return construir_resultado(
        level=nivel.stem,
        algorithm=nombre_algoritmo,
        heuristic=heuristica or "",
        busqueda=busqueda,
        time_ms=tiempo_ms,
        memory_mb=memoria_pico / (1024 * 1024),
    )


def guardar_csv(resultado: ResultadoEjecucion, ruta: str | Path) -> None:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    existe = ruta.exists() and ruta.stat().st_size > 0

    with ruta.open("a", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS_CSV)
        if not existe:
            writer.writeheader()

        fila = resultado.to_dict()
        fila["success"] = str(fila["success"]).lower()
        writer.writerow(fila)


def ejecutar_y_guardar(
    nivel: str | Path,
    algoritmo: str,
    heuristica: str | None,
    salida: str | Path,
    *,
    max_depth: int | None = None,
) -> ResultadoEjecucion:
    resultado = ejecutar(
        nivel,
        algoritmo,
        heuristica,
        max_depth=max_depth,
    )
    guardar_csv(resultado, salida)
    return resultado
