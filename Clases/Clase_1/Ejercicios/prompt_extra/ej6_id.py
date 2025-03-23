# Crea dos tuplas idénticas y verifica si comparten la misma dirección de memoria.

t1 = (1,2,3,4)
t2 = (1,2,3,4)

print(id(t1) == id(t2)) # las id son iguales, ya que las tuplas son inmutables, por lo que python reutiliza la direccion