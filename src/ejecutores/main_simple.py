import argparse

from .runner import ejecutar_y_guardar


def main():
    parser = argparse.ArgumentParser(
        description="Ejecuta un algoritmo de búsqueda sobre un nivel de Sokoban."
    )
    parser.add_argument("nivel", help="Ruta al archivo del nivel.")
    parser.add_argument(
        "algoritmo",
        choices=["bfs", "dfs", "greedy", "astar", "iddfs"],
    )
    parser.add_argument(
        "heuristica",
        nargs="?",
        default=None,
        help="manhattan o paredes_bfs. Requerida para greedy/astar.",
    )
    parser.add_argument(
        "--output",
        default="results/resultados.csv",
        help="CSV de salida.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Límite opcional de profundidad para IDDFS.",
    )

    args = parser.parse_args()

    if args.heuristica == "-":
        args.heuristica = None

    resultado = ejecutar_y_guardar(
        args.nivel,
        args.algoritmo,
        args.heuristica,
        args.output,
        max_depth=args.max_depth,
    )

    print(f"Nivel:              {resultado.level}")
    print(f"Algoritmo:          {resultado.algorithm}")
    print(f"Heurística:         {resultado.heuristic or '-'}")
    print(f"Éxito:              {resultado.success}")
    print(f"Costo:              {resultado.cost}")
    print(f"Nodos expandidos:   {resultado.nodes_expanded}")
    print(f"Nodos frontera:     {resultado.nodes_frontier}")
    print(f"Tiempo (ms):        {resultado.time_ms}")
    print(f"Memoria (MB):       {resultado.memory_mb}")
    print(f"Solución:           {resultado.solution or '-'}")
    print(f"Longitud solución:  {resultado.solution_length}")
    print(f"Guardado en:        {args.output}")


if __name__ == "__main__":
    main()
