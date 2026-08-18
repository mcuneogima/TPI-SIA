from pathlib import Path

import pandas as pd

from .utiles import guardar_tabla, graficar_barras_agrupadas


def analizar_nodos(df: pd.DataFrame, salida: Path) -> None:
    _analizar_metrica(df, "nodes_expanded", "Nodos expandidos", "nodos_expandidos", salida)
    _analizar_metrica(df, "nodes_frontier", "Nodos frontera", "nodos_frontera", salida)


def _analizar_metrica(
    df: pd.DataFrame,
    columna: str,
    titulo: str,
    nombre: str,
    salida: Path,
) -> None:
    por_metodo = (
        df.groupby("method", sort=False)[columna]
        .mean()
        .sort_values(ascending=False)
        .rename("mean")
        .reset_index()
    )
    guardar_tabla(por_metodo, salida / f"{nombre}_promedio_por_metodo.csv")

    por_nivel = df.pivot_table(
        index="method", columns="level", values=columna, aggfunc="mean"
    )
    guardar_tabla(por_nivel.reset_index(), salida / f"{nombre}_por_nivel.csv")

    graficar_barras_agrupadas(
        por_metodo.set_index("method"),
        f"{titulo} promedio por algoritmo y heurística",
        "Método",
        "Cantidad",
        salida / f"{nombre}_promedio_por_metodo.png",
        rotacion=45,
    )

    graficar_barras_agrupadas(
        por_nivel.T,
        f"{titulo} promedio por nivel",
        "Nivel",
        "Cantidad",
        salida / f"{nombre}_por_nivel.png",
        rotacion=45,
    )
