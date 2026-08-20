from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def preparar_salida(ruta: str | Path) -> Path:
    ruta = Path(ruta)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def guardar_grafico(fig, ruta: Path) -> None:
    fig.tight_layout()
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)


def guardar_tabla(df: pd.DataFrame, ruta: Path) -> None:
    df.to_csv(ruta, index=False, encoding="utf-8")


def graficar_barras_agrupadas(
    tabla: pd.DataFrame,
    titulo: str,
    eje_x: str,
    eje_y: str,
    ruta: Path,
    *,
    rotacion: int = 0,
    porcentaje: bool = False,
    errores: pd.DataFrame | None = None,
) -> None:
    """Grafica una tabla index x columnas como barras agrupadas.

    Si se proporciona ``errores``, debe tener los mismos índices y columnas
    que ``tabla``. Se utiliza como barra de error para cada media.
    """
    fig, ax = plt.subplots(figsize=(11, 6))

    plot_kwargs = {}
    if errores is not None:
        # Las barras sin suficientes observaciones tienen desviación estándar
        # NaN. Para el gráfico se muestran sin barra de error.
        errores_alineados = errores.reindex(
            index=tabla.index,
            columns=tabla.columns,
        ).fillna(0)
        plot_kwargs["yerr"] = errores_alineados
        plot_kwargs["capsize"] = 4

    tabla.plot(kind="bar", ax=ax, **plot_kwargs)
    ax.set_title(titulo)
    ax.set_xlabel(eje_x)
    ax.set_ylabel(eje_y)
    ax.tick_params(axis="x", rotation=rotacion)
    if porcentaje:
        ax.set_ylim(0, 100)
    ax.legend(title="Método")
    guardar_grafico(fig, ruta)
