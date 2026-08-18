import argparse
from pathlib import Path

from .carga import cargar_resultados
from .costos import analizar_costos
from .exito import analizar_exito
from .memoria import analizar_memoria
from .nodos import analizar_nodos
from .tiempos import analizar_tiempos


def ejecutar_analisis(csv: str | Path, salida: str | Path) -> None:
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)

    df = cargar_resultados(csv)

    # Guardamos una copia normalizada: resulta útil para verificar qué datos
    # fueron realmente consumidos por los analizadores.
    df.to_csv(salida / "datos_normalizados.csv", index=False, encoding="utf-8")

    analizar_tiempos(df, salida)
    analizar_memoria(df, salida)
    analizar_costos(df, salida)
    analizar_exito(df, salida)
    analizar_nodos(df, salida)

    print(f"Análisis completado: {salida.resolve()}")
    print(f"Ejecuciones analizadas: {len(df)}")
    print(f"Niveles: {df['level'].nunique()}")
    print(f"Métodos: {df['method'].nunique()}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analiza resultados de experimentos de Sokoban y genera CSVs y gráficos."
    )
    parser.add_argument("csv", help="CSV generado por la Etapa 1")
    parser.add_argument(
        "-o",
        "--output",
        default="analysis",
        help="Directorio de salida (default: analysis)",
    )
    args = parser.parse_args()

    ejecutar_analisis(args.csv, args.output)


if __name__ == "__main__":
    main()
