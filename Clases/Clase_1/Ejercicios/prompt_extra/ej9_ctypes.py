# Intenta modificar el valor de un entero pequeño (ej. 5) usando ctypes. ¿Qué ocurre?

import ctypes

value = 5
address = id(value)

try:
    ctypes.cast(address, ctypes.py_object).value = 10 
except Exception as e:
    print(e)

print(value) # el valor no se modifica


'''
Respuesta del apunte:
¡No se puede! Los enteros pequeños son inmutables y están internados.
Esto generaría un comportamiento indefinido.
'''