## Ejercicio 12: Ejecución Encadenada con `argparse` y Pipes

Implemente dos scripts:

1. `generador.py`: genera una serie de números aleatorios (parámetro `--n`) y los imprime por salida estándar.
2. `filtro.py`: recibe números por entrada estándar y muestra solo los mayores que un umbral (parámetro `--min`).

Desde Bash, encadene la salida del primero a la entrada del segundo:

```bash
generador.py --n 100 | filtro.py --min 50
```
---