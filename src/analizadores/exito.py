from pathlib import Path

import pandas as pd

from .utiles import guardar_tabla, graficar_barras_agrupadas


def analizar_exito(df: pd.DataFrame, salida: Path) -> None:
    resumen = (
        df.groupby("method", sort=False)["success"]
        .mean()
        .mul(100)
        .rename("success_rate_percent")
        .reset_index()
    )
    guardar_tabla(resumen, salida / "tasa_exito_por_metodo.csv")

    tabla = df.pivot_table(
        index="method", columns="level", values="success", aggfunc="mean"
    ).mul(100)
    guardar_tabla(tabla.reset_index(), salida / "tasa_exito_por_nivel.csv")

    graficar_barras_agrupadas(
        resumen.set_index("method"),
        "Tasa de éxito por algoritmo y heurística",
        "Método",
        "Éxito (%)",
        salida / "tasa_exito_por_metodo.png",
        rotacion=45,
        porcentaje=True,
    )

    graficar_barras_agrupadas(
        tabla.T,
        "Tasa de éxito por nivel",
        "Nivel",
        "Éxito (%)",
        salida / "tasa_exito_por_nivel.png",
        rotacion=45,
        porcentaje=True,
    )
