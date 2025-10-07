# Forma tradicional: toda la secuencia en memoria
def fibonacci_lista(n):
    resultado = []
    a, b = 0, 1
    for _ in range(n):
        resultado.append(a)
        a, b = b, a + b
    return resultado

# Forma con generador: un número a la vez
def fibonacci_generador(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Comparemos
lista = fibonacci_lista(100)      # Crea lista con 1 millón de números
gen = fibonacci_generador(100)    # Solo guarda dos variables: a y b

print(lista)

print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))

# El generador usa memoria constante, sin importar n

# Esto me permitiría hacer un generador infinito, sin explotar la memoria