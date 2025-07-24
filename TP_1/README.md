> Trabajo realizado por Valentino Perassi Ferrara


# TP1 - Monitoreo Biométrico Distribuido y Blockchain

Este proyecto implementa un sistema de monitoreo biométrico distribuido que simula la recolección, análisis, verificación y almacenamiento seguro de datos (frecuencia cardíaca, presión sistólica y oxígeno en sangre) utilizando **procesos concurrentes** y una **cadena de bloques (blockchain)** que permite verificar la integridad de los datos y obtener un **reporte final** de los resultados.

---

## Requisitos

- Python 3.9 o superior.

---

## Ejecución

**Programa Principal**

```bash
python3 main.py
```

**Verificación de Integridad y Generación de Reporte**

```bash
python3 verificar_cadena.py
```

----


### Archivos Generados

Al ejecutar el programa, se crearán los siguientes archivos:

  * **`blockchain.json`**: Contiene la cadena de bloques completa con los datos biométricos procesados, sus hashes, y las alertas correspondientes. Este archivo se actualiza en tiempo real.
  * **`reporte.txt`**: Un archivo de texto que resume el análisis de la blockchain, incluyendo la cantidad total de bloques, bloques con alertas y promedios generales de las variables.

---

### Consideraciones

  * La simulación se ejecuta por 60 segundos por defecto (definido en la función `generator`).
  * La ventana móvil de los analizadores es de 30 segundos.
  * La presión solo considera el valor **sistólico** para el análisis y almacenamiento en la blockchain.
  * El cálculo del hash del bloque asegura la inmutabilidad y la integridad de la cadena.