# Enunciado: Crea un objeto en Python, obtén su id() y, usando ctypes, recupera una referencia al mismo.
# Luego, elimina la referencia original y verifica qué ocurre si intentas seguir utilizando la dirección.

import ctypes
import gc

variable = [1,2,3]

addr = id(variable)

copy = ctypes.cast(addr, ctypes.py_object).value

print(addr)
print(copy)

del variable # tras esto, el objeto puede ser liberado, lo cual es peligroso
gc.collect() # fuerzo la recoleccion de basura, que libera el objeto

try:
    addr = id(variable) # al intentar obtener la id del objeto liberado, da error porque ya no existe
    copy = ctypes.cast(addr, ctypes.py_object).value
except Exception as e:
    print(e)