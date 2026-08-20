# Sokoban

Motor de búsqueda de Sokoban implementado en Python sin librerías que resuelvan el problema.

## Requisitos

- Python 3.10+.
- pandas >= 2.0
- numpy >= 1.24
- matplotlib >= 3.7

(correr pip install -r requirements.txt para bajar dependencias)

## Estructura

```text
levels/                  niveles de entrada
src/
  modelos/               mapa, estado, acciones y parser
  algoritmos/            BFS, DFS, Greedy, A*, IDDFS
  heuristicas/           Manhattan y distancias de empuje con BFS
  ejecutores/            CLI simple y ejecución múltiple
  resultados/            estructuras de resultados
  analizadores/          generadores de graficos y csv's
results/                 CSV generado por las ejecuciones
analysis/                carpeta destino de graficos
```

## Formato de nivel

```text
#######
#     #
# .$. #
#  @  #
#######
```

Símbolos:

- `#`: pared
- espacio: suelo
- `.`: objetivo
- `$`: caja
- `@`: jugador
- `*`: caja sobre objetivo
- `+`: jugador sobre objetivo

Todas las filas deben tener el mismo ancho. Un nivel estándar tiene la misma cantidad de cajas y objetivos, aunque el parser no lo impone.

## Ejecutar una instancia

Desde la raíz del proyecto:

```bash
python -m src.ejecutores.main_simple levels/level01.txt astar manhattan
```

Ejemplos:

```bash
python -m src.ejecutores.main_simple levels/level01.txt bfs
python -m src.ejecutores.main_simple levels/level01.txt dfs
python -m src.ejecutores.main_simple levels/level01.txt greedy paredes_bfs
python -m src.ejecutores.main_simple levels/level01.txt astar paredes_bfs
python -m src.ejecutores.main_simple levels/level01.txt iddfs
```

El resultado se agrega a `results/resultados.csv`.

## Ejecutar N veces

```bash
python -m src.ejecutores.ejecutor_multiple levels/level01.txt astar manhattan 10
```

Para algoritmos sin heurística:

```bash
python -m src.ejecutores.ejecutor_multiple levels/level01.txt bfs - 10
```

Para probar todos los algoritmos N veces para niveles 1-3:
```bash
python ejecutar_experimentos.py --runs 10
```

## Métricas

Cada ejecución registra:

- nivel
- algoritmo
- heurística
- éxito
- costo de la solución
- longitud de la solución
- nodos expandidos
- tamaño de la frontera al terminar
- tiempo de ejecución
- memoria máxima medida por `tracemalloc`
- solución como secuencia de acciones

El costo es el número de movimientos del jugador. Caminar y empujar cuentan como un movimiento.

Para generar graficos con la información en results correr:
```bash
python -m src.analizadores.analizar results/resultados.csv -o analysis
```

## Heurísticas

### Manhattan

Para cada caja se calcula la distancia Manhattan a cada objetivo y se busca el emparejamiento de costo mínimo. Es admisible porque ignora paredes, otras cajas y la necesidad de posicionar al jugador.

### Distancia de empuje con BFS

Para cada objetivo se precalculan las distancias mínimas de empuje de una caja, considerando únicamente las paredes. Las otras cajas y el jugador se ignoran durante este cálculo. El costo de la asignación mínima entre cajas y objetivos es una cota inferior del número de movimientos reales, por lo que también es admisible para el costo de movimientos.

## Sobre DFS e IDDFS

DFS usa un conjunto de visitados para evitar ciclos. El orden de acciones es fijo (`UP`, `RIGHT`, `DOWN`, `LEFT`), por lo que una ejecución es reproducible.

IDDFS realiza búsquedas con límite creciente de profundidad. Como la unidad de costo es un movimiento, la profundidad coincide con el costo de la solución.

## Frontera

`nodes_frontier` representa la cantidad de nodos que permanecen en la estructura de frontera cuando termina la búsqueda. Para análisis de uso máximo de frontera puede agregarse posteriormente una métrica independiente.
