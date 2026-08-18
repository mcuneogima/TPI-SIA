import argparse
import csv
import subprocess
import sys
from pathlib import Path


# Directorios
ROOT_DIR = Path(__file__).resolve().parent
LEVELS_DIR = ROOT_DIR / "levels"
RESULTS_FILE = ROOT_DIR / "results" / "resultados.csv"
EXECUTOR = ROOT_DIR / "src" / "ejecutores" / "ejecutor_multiple.py"
DEFAULT_TIMEOUT = 60

# Combinaciones a ejecutar.
#
# None significa que el algoritmo no utiliza heurística.
EXPERIMENTS = [
    ("bfs", None),
    ("dfs", None),
    ("greedy", "manhattan"),
    ("greedy", "paredes"),
    ("astar", "manhattan"),
    ("astar", "paredes"),
    ("iddfs", None),
]


def limpiar_resultados():
    """Elimina los resultados de ejecuciones anteriores."""

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    if RESULTS_FILE.exists():
        RESULTS_FILE.unlink()
        print(f"[LIMPIEZA] Eliminado: {RESULTS_FILE}")
    else:
        print(f"[LIMPIEZA] No existía: {RESULTS_FILE}")


def ejecutar(nivel, algoritmo, heuristica, timeout):
    """Ejecuta una única ejecución de un algoritmo."""

    heuristica_arg = heuristica if heuristica is not None else "-"

    nivel_arg = nivel.relative_to(ROOT_DIR)

    comando = [
        sys.executable,
        "-m",
        "src.ejecutores.ejecutor_multiple",
        str(nivel_arg),
        algoritmo,
        heuristica_arg,
        "1",
    ]

    nombre_heuristica = heuristica if heuristica else "-"

    print(
        f"\n[RUN] "
        f"nivel={nivel.stem} | "
        f"algoritmo={algoritmo} | "
        f"heuristica={nombre_heuristica} | "
        f"timeout={timeout}s"
    )

    try:
        resultado = subprocess.run(
            comando,
            cwd=ROOT_DIR,
            timeout=timeout,
        )

    except subprocess.TimeoutExpired:
        print(
            f"[TIMEOUT] "
            f"{nivel.stem} / {algoritmo} / {nombre_heuristica} "
            f"superó los {timeout}s"
        )

        guardar_timeout(
            nivel=nivel,
            algoritmo=algoritmo,
            heuristica=heuristica,
            timeout=timeout,
        )

        return False

    if resultado.returncode != 0:
        print(
            f"[ERROR] Falló la ejecución: "
            f"{nivel.stem} / {algoritmo} / {nombre_heuristica}"
        )
        return False

    print("[OK]")
    return True


def guardar_timeout(nivel, algoritmo, heuristica, timeout):
    """Guarda una ejecución que superó el límite de tiempo."""

    heuristica_arg = heuristica if heuristica is not None else ""

    fila = {
        "level": nivel.stem,
        "algorithm": algoritmo,
        "heuristic": heuristica_arg,
        "success": False,
        "cost": "",
        "solution_length": "",
        "nodes_expanded": "",
        "nodes_frontier": "",
        "time": timeout * 1000,
        "memory": "",
        "solution": "",
    }

    archivo = RESULTS_FILE

    existe = archivo.exists()

    with archivo.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fila.keys(),
        )

        if not existe:
            writer.writeheader()

        writer.writerow(fila)

    print(f"[TIMEOUT] Resultado guardado en {archivo}")

def main():
    parser = argparse.ArgumentParser(
        description="Ejecuta todos los experimentos de Sokoban."
    )

    parser.add_argument(
        "-n",
        "--runs",
        type=int,
        default=1,
        help="Cantidad de ejecuciones por combinación (default: 1).",
    )

    parser.add_argument(
        "--desde",
        type=int,
        default=1,
        choices=[1, 2, 3],
        help="Primer nivel a ejecutar (default: 1).",
    )

    parser.add_argument(
        "--hasta",
        type=int,
        default=3,
        choices=[1, 2, 3],
        help="Último nivel a ejecutar (default: 3).",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Tiempo máximo en segundos por ejecución (default: 60).",
    )

    args = parser.parse_args()

    if args.runs <= 0:
        parser.error("--runs debe ser mayor que 0")

    if args.desde > args.hasta:
        parser.error("--desde no puede ser mayor que --hasta")

    # Verificaciones
    if not LEVELS_DIR.exists():
        print(f"[ERROR] No existe el directorio: {LEVELS_DIR}")
        sys.exit(1)

    if not EXECUTOR.exists():
        print(f"[ERROR] No existe el ejecutor: {EXECUTOR}")
        sys.exit(1)

    niveles = [
        LEVELS_DIR / f"level{i:02d}.txt"
        for i in range(args.desde, args.hasta + 1)
    ]

    niveles_faltantes = [
        nivel for nivel in niveles
        if not nivel.exists()
    ]

    if niveles_faltantes:
        print("[ERROR] No se encontraron los siguientes niveles:")

        for nivel in niveles_faltantes:
            print(f"  - {nivel}")

        sys.exit(1)

    # ---------------------------------------------------------
    # 1. Limpiar resultados anteriores
    # ---------------------------------------------------------

    limpiar_resultados()

    # ---------------------------------------------------------
    # 2. Ejecutar experimentos
    # ---------------------------------------------------------

    total = len(niveles) * len(EXPERIMENTS)

    print("\n" + "=" * 70)
    print("INICIO DE EXPERIMENTOS")
    print("=" * 70)
    print(f"Niveles:      {len(niveles)}")
    print(f"Combinaciones: {len(EXPERIMENTS)}")
    print(f"Ejecuciones:  {args.runs}")
    print(f"Total:         {total} combinaciones")
    print("=" * 70)

    exitosas = 0
    fallidas = 0

    contador = 0

    for nivel in niveles:
        for algoritmo, heuristica in EXPERIMENTS:
            contador += 1

            print(
                f"\n[{contador}/{total}] "
                f"{nivel.stem} - {algoritmo}"
                + (
                    f" - {heuristica}"
                    if heuristica
                    else ""
                )
            )

            for ejecucion in range(1, args.runs + 1):
                print(
                    f"\n    Ejecución {ejecucion}/{args.runs}"
                )

                ok = ejecutar(
                    nivel=nivel,
                    algoritmo=algoritmo,
                    heuristica=heuristica,
                    timeout=args.timeout,
                )

                if ok:
                    exitosas += 1
                else:
                    fallidas += 1

    # ---------------------------------------------------------
    # 3. Resumen
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("EXPERIMENTOS FINALIZADOS")
    print("=" * 70)
    print(f"Combinaciones exitosas: {exitosas}")
    print(f"Combinaciones fallidas: {fallidas}")
    print(f"Resultados:             {RESULTS_FILE}")

    if RESULTS_FILE.exists():
        print(
            f"Tamaño del CSV:          "
            f"{RESULTS_FILE.stat().st_size / 1024:.2f} KB"
        )

    print("=" * 70)


if __name__ == "__main__":
    main()