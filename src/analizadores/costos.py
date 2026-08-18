from pathlib import Path

import numpy as np
import pandas as pd

from .utiles import guardar_tabla, graficar_barras_agrupadas


def analizar_costos(df: pd.DataFrame, salida: Path) -> pd.DataFrame:
    exitosos = df[df["success"] & df["cost"].notna()].copy()

    resumen = (
        exitosos.groupby("method", sort=False)["cost"]
        .mean()
        .sort_values()
        .rename("cost_mean")
        .reset_index()
    )
    guardar_tabla(resumen, salida / "costo_promedio_por_metodo.csv")

    tabla_nivel = exitosos.pivot_table(
        index="method", columns="level", values="cost", aggfunc="mean"
    )
    guardar_tabla(tabla_nivel.reset_index(), salida / "costo_por_nivel.csv")

    graficar_barras_agrupadas(
        resumen.set_index("method"),
        "Costo promedio de solución",
        "Método",
        "Movimientos",
        salida / "costo_promedio_por_metodo.png",
        rotacion=45,
    )

    graficar_barras_agrupadas(
        tabla_nivel.T,
        "Costo promedio por nivel",
        "Nivel",
        "Movimientos",
        salida / "costo_por_nivel.png",
        rotacion=45,
    )

    relativos = calcular_costo_relativo(exitosos)
    guardar_tabla(relativos, salida / "costo_relativo_al_optimo.csv")

    tabla_rel = relativos.pivot_table(
        index="method", columns="level", values="relative_cost", aggfunc="mean"
    )
    guardar_tabla(tabla_rel.reset_index(), salida / "costo_relativo_por_nivel.csv")

    graficar_barras_agrupadas(
        tabla_rel.T,
        "Costo relativo al óptimo por nivel",
        "Nivel",
        "Costo / óptimo",
        salida / "costo_relativo_por_nivel.png",
        rotacion=45,
    )

    return relativos


def calcular_costo_relativo(exitosos: pd.DataFrame) -> pd.DataFrame:
    """
    Define el óptimo experimental de cada nivel como el menor costo exitoso
    observado en el CSV. Si se ejecutó BFS/otro método óptimo exhaustivo,
    normalmente coincidirá con el óptimo real.
    """
    if exitosos.empty:
        return pd.DataFrame(
            columns=["level", "method", "cost", "optimal_cost", "relative_cost"]
        )

    optimos = exitosos.groupby("level")["cost"].min().rename("optimal_cost")
    resultado = exitosos[["level", "method", "cost"]].copy()
    resultado = resultado.join(optimos, on="level")
    resultado["relative_cost"] = np.where(
        resultado["optimal_cost"] > 0,
        resultado["cost"] / resultado["optimal_cost"],
        np.nan,
    )
    return resultado
