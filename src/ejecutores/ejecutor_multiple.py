import argparse

from .runner import ejecutar_y_guardar


def main():
    parser = argparse.ArgumentParser(
        description="Ejecuta N veces un experimento de Sokoban y agrega "
                    "una fila por ejecución al CSV."
    )
    parser.add_argument("nivel")
    parser.add_argument(
        "algoritmo",
        choices=["bfs", "dfs", "greedy", "astar", "iddfs"],
    )
    parser.add_argument(
        "heuristica",
        help="manhattan, paredes_bfs o '-' si no aplica.",
    )
    parser.add_argument(
        "cantidad",
        type=int,
        help="Cantidad de ejecuciones.",
    )
    parser.add_argument(
        "--output",
        default="results/resultados.csv",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
    )

    args = parser.parse_args()

    if args.cantidad <= 0:
        parser.error("La cantidad de ejecuciones debe ser mayor que 0.")

    heuristica = None if args.heuristica == "-" else args.heuristica

    for i in range(1, args.cantidad + 1):
        resultado = ejecutar_y_guardar(
            args.nivel,
            args.algoritmo,
            heuristica,
            args.output,
            max_depth=args.max_depth,
        )
        print(
            f"[{i}/{args.cantidad}] "
            f"success={resultado.success} "
            f"cost={resultado.cost} "
            f"expanded={resultado.nodes_expanded} "
            f"time_ms={resultado.time_ms}"
        )


if __name__ == "__main__":
    main()
