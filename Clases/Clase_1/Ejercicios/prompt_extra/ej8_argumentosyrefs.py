# Escribe una función que reciba una lista y devuelva una copia modificada sin alterar la original.

def modify_list(lista):
    lista2 = lista.copy() # metodo copy para clonar la lista
    lista2.append(900)
    return lista2

lista = [1,2,3]

lista2 = modify_list(lista)

print(lista) # original
print(lista2) # copia modificada

id_vieja = id(lista)
id_nueva = id(lista2)

print (lista == lista2)
print (id_vieja == id_nueva) # la id se modifico porque la copia modificada es un objeto distinto a la original