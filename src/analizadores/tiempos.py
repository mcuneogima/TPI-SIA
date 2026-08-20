from pathlib import Path

import pandas as pd

from .utiles import guardar_tabla, graficar_barras_agrupadas


def _estadisticas(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    agrupado = df.groupby("method", sort=False)["time_ms"]
    medias = agrupado.mean().rename("time_ms_mean")
    errores = agrupado.std().rename("time_ms_std")
    return medias.reset_index(), errores.reset_index()


def analizar_tiempos(df: pd.DataFrame, salida: Path) -> None:
    resumen, error_resumen = _estadisticas(df)

    resumen = resumen.sort_values(
        "time_ms_mean",
        ascending=False,
    )

    error_resumen = (
        error_resumen
        .set_index("method")
        .reindex(resumen["method"])
    )

    # ---------------------------------------------------------
    # Tabla completa: promedio + desviación estándar
    # ---------------------------------------------------------

    resumen_completo = resumen.set_index("method").join(
        error_resumen
    )

    guardar_tabla(
        resumen_completo.reset_index(),
        salida / "tiempo_promedio_por_metodo.csv",
    )

    # ---------------------------------------------------------
    # Tiempo por nivel
    # ---------------------------------------------------------

    medias_nivel = df.pivot_table(
        index="method",
        columns="level",
        values="time_ms",
        aggfunc="mean",
    )

    errores_nivel = df.pivot_table(
        index="method",
        columns="level",
        values="time_ms",
        aggfunc="std",
    )

    guardar_tabla(
        medias_nivel.reset_index(),
        salida / "tiempo_por_nivel.csv",
    )

    guardar_tabla(
        errores_nivel.reset_index(),
        salida / "tiempo_error_por_nivel.csv",
    )

    # ---------------------------------------------------------
    # Gráfico: tiempo por nivel
    # ---------------------------------------------------------

    graficar_barras_agrupadas(
        medias_nivel.T,
        "Tiempo promedio por nivel",
        "Nivel",
        "Tiempo (ms)",
        salida / "tiempo_por_nivel.png",
        rotacion=45,
        errores=errores_nivel.T,
    )

    # ---------------------------------------------------------
    # Gráfico: tiempo promedio por método
    # ---------------------------------------------------------

    tabla_grafico = resumen.set_index("method")

    # IMPORTANTE:
    # yerr debe tener exactamente la misma estructura que
    # tabla_grafico: mismo índice y mismas columnas.
    errores_grafico = pd.DataFrame(
        {
            "time_ms_mean": error_resumen["time_ms_std"]
        },
        index=error_resumen.index,
    )

    graficar_barras_agrupadas(
        tabla_grafico,
        "Tiempo promedio por algoritmo y heurística",
        "Método",
        "Tiempo (ms)",
        salida / "tiempo_promedio_por_metodo.png",
        rotacion=45,
        errores=errores_grafico,
    )
