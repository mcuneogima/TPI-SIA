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
) -> None:
    """Grafica una tabla index x columnas como barras agrupadas."""
    fig, ax = plt.subplots(figsize=(11, 6))
    tabla.plot(kind="bar", ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(eje_x)
    ax.set_ylabel(eje_y)
    ax.tick_params(axis="x", rotation=rotacion)
    if porcentaje:
        ax.set_ylim(0, 100)
    ax.legend(title="Método")
    guardar_grafico(fig, ruta)
