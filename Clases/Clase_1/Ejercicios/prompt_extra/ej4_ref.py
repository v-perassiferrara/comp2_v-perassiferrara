import sys

a = [1, 2, 3]

b = a

print(sys.getrefcount(a))
print(sys.getrefcount(b))

# hay 3 referencias al mismo objeto, y ambos valores son iguales porque apuntan al mismo objeto