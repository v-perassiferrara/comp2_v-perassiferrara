def funcion():
    yield 1
    yield 2
    yield 3
 
print(type(funcion()))    
print(funcion())
print(next(funcion()))
print(next(funcion()))
print(next(funcion()))


print("si asigno la funcion a una variable, se convierte en un generador")

g = funcion()   # este objeto representa la funcion

print(type(g))
print(next(g))
print(next(g))
print(next(g))