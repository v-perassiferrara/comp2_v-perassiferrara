# Crea un sistema que:
# Genere un objeto mutable (ej. lista) y uno inmutable (ej. tupla).
# Pásalos a una función y observa los cambios.
# Usa sys.getrefcount para rastrear referencias.
# Intenta (con cuidado) modificar un objeto usando ctypes.

import ctypes
import sys

def cambiar_objeto(objeto):
    objeto[3] = "hola"
    objeto.append("255")

# Genere un objeto mutable (ej. lista) y uno inmutable (ej. tupla).
lista = [1,2,3,4]
tupla = (1,2,3,4)

#estado inicial
print(lista)
print(tupla)


# Usa sys.getrefcount para rastrear referencias.
print(sys.getrefcount(lista))
print(sys.getrefcount(tupla))

try:
    cambiar_objeto(lista) # la lista es mutable, se modifica
    cambiar_objeto(tupla) # la tupla es inmutable: la funcion da error y la tupla no se modifica
except Exception as e:
    print(e)

#estado final
print(lista)
print(tupla)

# Usa sys.getrefcount para rastrear referencias.
print(sys.getrefcount(lista))
print(sys.getrefcount(tupla))

# Intenta (con cuidado) modificar un objeto usando ctypes.

address = id(lista)

ctypes.cast(address, ctypes.py_object).value.append(14)

print(lista) # la lista se modifico

# los objetos inmutables no pueden modificarse ni siquiera con ctypes porque python bloquea su espacio de memoria