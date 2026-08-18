from pathlib import Path

import pandas as pd

from .utiles import guardar_tabla, graficar_barras_agrupadas


def analizar_tiempos(df: pd.DataFrame, salida: Path) -> None:
    resumen = (
        df.groupby("method", sort=False)["time_ms"]
        .mean()
        .sort_values(ascending=False)
        .rename("time_ms_mean")
        .reset_index()
    )
    guardar_tabla(resumen, salida / "tiempo_promedio_por_metodo.csv")

    tabla = df.pivot_table(
        index="method", columns="level", values="time_ms", aggfunc="mean"
    )
    guardar_tabla(tabla.reset_index(), salida / "tiempo_por_nivel.csv")

    graficar_barras_agrupadas(
        tabla.T,
        "Tiempo promedio por nivel",
        "Nivel",
        "Tiempo (ms)",
        salida / "tiempo_por_nivel.png",
        rotacion=45,
    )

    fig_tabla = resumen.set_index("method")
    graficar_barras_agrupadas(
        fig_tabla,
        "Tiempo promedio por algoritmo y heurística",
        "Método",
        "Tiempo (ms)",
        salida / "tiempo_promedio_por_metodo.png",
        rotacion=45,
    )
