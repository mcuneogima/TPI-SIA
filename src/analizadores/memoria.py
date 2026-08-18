from pathlib import Path

import pandas as pd

from .utiles import guardar_tabla, graficar_barras_agrupadas


def analizar_memoria(df: pd.DataFrame, salida: Path) -> None:
    resumen = (
        df.groupby("method", sort=False)["memory_mb"]
        .mean()
        .sort_values(ascending=False)
        .rename("memory_mb_mean")
        .reset_index()
    )
    guardar_tabla(resumen, salida / "memoria_promedio_por_metodo.csv")

    tabla = df.pivot_table(
        index="method", columns="level", values="memory_mb", aggfunc="mean"
    )
    guardar_tabla(tabla.reset_index(), salida / "memoria_por_nivel.csv")

    graficar_barras_agrupadas(
        resumen.set_index("method"),
        "Memoria promedio por algoritmo y heurística",
        "Método",
        "Memoria (MB)",
        salida / "memoria_promedio_por_metodo.png",
        rotacion=45,
    )

    graficar_barras_agrupadas(
        tabla.T,
        "Memoria promedio por nivel",
        "Nivel",
        "Memoria (MB)",
        salida / "memoria_por_nivel.png",
        rotacion=45,
    )
