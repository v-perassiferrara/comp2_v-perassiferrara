from tasks import sumar, tarea_larga

# Ejecutar tarea de forma asíncrona
result = sumar.delay(4, 6) # encolo la tarea con el método delay, que todas las tareas tienen
# este result es una promesa/futuro, su tipo es "async result"

result2 = tarea_larga.delay()

# Continuar sin esperar
print("Tarea enviada, continuando...")

# Obtener resultado (esto bloquea hasta que termine)
print(f"Resultado: {result.get(timeout=10)}")

try:
    print(f"Resultado: {result2.get(timeout=10)}")
except Exception as e:
    print(f"Error: {e}")