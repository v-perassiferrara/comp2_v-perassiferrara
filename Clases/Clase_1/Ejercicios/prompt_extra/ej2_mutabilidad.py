# Enunciado: Diseña una función modificar_elemento que reciba una lista y cambie su primer elemento a 999.
# Prueba luego con una tupla y explica qué sucede.

def modificar_elemento(list):
    list[0] = 999

list_1 = [1,2,3,4]
tuple_1 = (1,2,3,4)

print(list_1)
print(tuple_1)

try:
    modificar_elemento(list_1)
    modificar_elemento(tuple_1)
except Exception as e:
    print(e)

print(list_1) # se modifica el primer elemento porque es un objeto mutable
print(tuple_1) # no se modifica porque es inmutable