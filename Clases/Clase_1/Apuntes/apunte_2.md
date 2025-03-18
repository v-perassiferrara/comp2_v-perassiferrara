# Apunte: Manejo de Argumentos en Python con `getopt` y `argparse`

## 📌 Conceptos Clave

### 1. **Argumentos de Línea de Comandos**
- **Definición**: Valores pasados a un script al ejecutarlo desde la terminal.
- **Ejemplo**:  
  ```bash
  python script.py --input archivo.txt --output resultado.txt
  ```
- **Usos**:
  - Personalizar la ejecución de scripts.
  - Automatizar tareas.
  - Integrar con otros programas.

---

### 2. **Módulos para Parsear Argumentos**
#### 🔹 `getopt`
- **Origen**: Basado en la función `getopt()` de C.
- **Uso**: Para scripts simples con pocas opciones.
- **Ejemplo**:
  ```python
  import getopt, sys

  opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["input=", "output="])
  ```
  - **`i:o:`**: Opciones cortas (`-i valor`, `-o valor`).
  - **`["input=", "output="]`**: Opciones largas (`--input valor`, --output valor`).

#### 🔸 `argparse`
- **Ventajas**:
  - Mensajes de ayuda automáticos (`-h`).
  - Validación integrada (tipos, obligatoriedad, etc.).
  - Soporta subcomandos y argumentos posicionales.
- **Ejemplo básico**:
  ```python
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", required=True, help="Archivo de entrada")
  args = parser.parse_args()
  ```

---

## 🛠️ Diferencias entre `getopt` y `argparse`
| **Característica**      | `getopt`                          | `argparse`                          |
|-------------------------|-----------------------------------|-------------------------------------|
| Complejidad             | Baja (para casos simples)         | Alta (para scripts complejos)       |
| Validación              | Manual                            | Automática                          |
| Mensajes de ayuda       | Requiere código adicional         | Generados automáticamente           |
| Flexibilidad            | Limitada                          | Alta (soporta tipos, subcomandos, etc.) |

---

## 💻 Ejemplos Prácticos

### 1. **Script con `argparse`**
```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Procesar archivos")
    parser.add_argument("-f", "--file", required=True, help="Archivo de entrada")
    parser.add_argument("-n", "--lines", type=int, default=5, help="Líneas a mostrar")
    parser.add_argument("-r", "--reverse", action="store_true", help="Invertir orden")
    
    args = parser.parse_args()
    
    with open(args.file, "r") as f:
        lineas = f.readlines()
    
    lineas = lineas[:args.lines]
    if args.reverse:
        lineas = lineas[::-1]  # Invertir con slicing
    
    print("".join(lineas))

if __name__ == "__main__":
    main()
```

---

### 2. **Manejo de Errores Comunes**

#### 🔴 `TypeError: 'NoneType' object is not subscriptable`
- **Causa**: Usar `lista = lista.reverse()` (el método `reverse()` devuelve `None`).
- **Solución**: Usar slicing `[::-1]` o no reasignar:  
  ```python
  lista.reverse()  # Modifica la lista original
  # O
  lista = lista[::-1]  # Crea una copia invertida
  ```

---

## 🔧 Funcionalidades Avanzadas de `argparse`
### 1. **Argumentos Posicionales vs. Opcionales**
| **Tipo**          | Ejemplo                  | Definición en `argparse`            |
|--------------------|--------------------------|--------------------------------------|
| Posicional         | `python script.py archivo` | `parser.add_argument("archivo")`    |
| Opcional           | `python script.py -f archivo` | `parser.add_argument("-f", "--file")` |

### 2. **Validación con `choices`**
```python
parser.add_argument("--modo", choices=["rapido", "lento"], help="Modo de ejecución")
```
- Si el usuario pasa un valor no válido, `argparse` muestra un error automático.

### 3. **Flags Booleanos (`action="store_true"`)**
```python
parser.add_argument("-v", "--verbose", action="store_true", help="Modo detallado")
```

---

## 📚 Recursos Adicionales
1. **Documentación Oficial**:
   - [`argparse`](https://docs.python.org/3/library/argparse.html)
   - [`getopt`](https://docs.python.org/3/library/getopt.html)
2. **Tutoriales**:
   - [Real Python: Command-Line Interfaces](https://realpython.com/command-line-interfaces-python-argparse/)
   - [Argparse Tutorial Oficial](https://docs.python.org/3/howto/argparse.html)