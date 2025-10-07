def contar_hasta_tres():
    print("Voy a producir el 1")
    yield 1
    print("Voy a producir el 2")
    yield 2
    print("Voy a producir el 3")
    yield 3
    print("Ya no tengo más números")

contador = contar_hasta_tres()

print(contador)

print(next(contador))  
# Imprime: "Voy a producir el 1"
# Devuelve: 1

print(next(contador))  
# Imprime: "Voy a producir el 2"
# Devuelve: 2

print(next(contador))  
# Imprime: "Voy a producir el 3"
# Devuelve: 3

print(next(contador))  
# Imprime: "Ya no tengo más números"
# Lanza: StopIteration