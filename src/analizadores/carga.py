from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "level",
    "algorithm",
    "heuristic",
    "success",
    "cost",
    "nodes_expanded",
    "nodes_frontier",
    "time_ms",
    "memory_mb",
}


def cargar_resultados(ruta: str | Path) -> pd.DataFrame:
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el CSV: {ruta}")

    df = pd.read_csv(ruta)
    faltantes = REQUIRED_COLUMNS - set(df.columns)
    if faltantes:
        raise ValueError(
            "El CSV no contiene las columnas requeridas: "
            + ", ".join(sorted(faltantes))
        )

    df = df.copy()

    # Normalizamos valores para que el análisis sea independiente de cómo
    # fueron escritos en el CSV.
    df["algorithm"] = df["algorithm"].fillna("").astype(str).str.strip().str.lower()
    df["heuristic"] = df["heuristic"].fillna("").astype(str).str.strip().str.lower()
    df["level"] = df["level"].astype(str).str.strip()

    if df["success"].dtype == bool:
        pass
    else:
        df["success"] = (
            df["success"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({"true": True, "false": False, "1": True, "0": False})
        )

    for column in [
        "cost",
        "nodes_expanded",
        "nodes_frontier",
        "time_ms",
        "memory_mb",
    ]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Para los gráficos es más útil mostrar nombres humanos.
    df["method"] = df.apply(_nombre_metodo, axis=1)
    return df


def _nombre_metodo(row: pd.Series) -> str:
    algorithm = row["algorithm"]
    heuristic = row["heuristic"]

    nombres = {
        "bfs": "BFS",
        "dfs": "DFS",
        "greedy": "Greedy",
        "astar": "A*",
        "a*": "A*",
        "iddfs": "IDDFS",
    }
    algoritmo = nombres.get(algorithm, algorithm.upper())

    if algorithm in {"greedy", "astar", "a*"} and heuristic:
        heuristicas = {
            "manhattan": "Manhattan",
            "paredes_bfs": "Paredes BFS",
        }
        return f"{algoritmo} - {heuristicas.get(heuristic, heuristic)}"

    return algoritmo
