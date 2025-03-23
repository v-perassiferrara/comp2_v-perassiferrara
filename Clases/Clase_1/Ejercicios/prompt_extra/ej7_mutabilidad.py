# Crea un diccionario y una tupla. Intenta modificar ambos y observa los errores.

a = {1:2}

b = (1,2)

try:
    a[1] = 3
    b[1] = 3
except Exception as e:
    print(e)

print(a) # no se modifico el segundo valor almacenado
print(b) # se modifico el valor de la key "1"