# Enunciado: Crea dos listas diferentes pero con el mismo contenido.
# Imprime sus direcciones de memoria y verifica si son iguales o distintas.

list_1 = [1,2,3]
list_2 = [1,2,3]

print(id(list_1))
print(id(list_2))

print (list_1 == list_2) #contenido igual o distinto
print(id(list_1) == id(list_2)) #ids iguales o distintas
print (list_1 is list_2) #objetos iguales o distintos