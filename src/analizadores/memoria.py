from pathlib import Path

import pandas as pd

from .utiles import guardar_tabla, graficar_barras_agrupadas


def analizar_memoria(df: pd.DataFrame, salida: Path) -> None:
    agrupado = df.groupby("method", sort=False)["memory_mb"]
    resumen = (
        agrupado.mean()
        .sort_values(ascending=False)
        .rename("memory_mb_mean")
        .reset_index()
    )
    errores_resumen = agrupado.std().rename("memory_mb_std").to_frame()
    errores_resumen = errores_resumen.reindex(resumen["method"])

    guardar_tabla(
        resumen.set_index("method").join(errores_resumen).reset_index(),
        salida / "memoria_promedio_por_metodo.csv",
    )

    medias_nivel = df.pivot_table(
        index="method", columns="level", values="memory_mb", aggfunc="mean"
    )
    errores_nivel = df.pivot_table(
        index="method", columns="level", values="memory_mb", aggfunc="std"
    )
    guardar_tabla(
        medias_nivel.reset_index(),
        salida / "memoria_por_nivel.csv",
    )
    guardar_tabla(
        errores_nivel.reset_index(),
        salida / "memoria_error_por_nivel.csv",
    )

    graficar_barras_agrupadas(
        resumen.set_index("method"),
        "Memoria promedio por algoritmo y heurística",
        "Método",
        "Memoria (MB)",
        salida / "memoria_promedio_por_metodo.png",
        rotacion=45,
        errores=errores_resumen,
    )

    graficar_barras_agrupadas(
        medias_nivel.T,
        "Memoria promedio por nivel",
        "Nivel",
        "Memoria (MB)",
        salida / "memoria_por_nivel.png",
        rotacion=45,
        errores=errores_nivel.T,
    )
