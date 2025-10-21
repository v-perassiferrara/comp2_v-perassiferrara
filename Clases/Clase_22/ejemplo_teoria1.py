from concurrent.futures import ThreadPoolExecutor
import time

def tarea_lenta(n):
    time.sleep(8)
    return n * 2

executor = ThreadPoolExecutor(max_workers=2)

# submit() retorna un Future inmediatamente
future = executor.submit(tarea_lenta, 10)

print(f"Future creado: {future}")
print(f"¿Está corriendo? {future.running()}")
print(f"¿Terminó? {future.done()}")

# result() bloquea hasta que termine
try:
    resultado = future.result(2)  # Espera ~2s como máximo
except TimeoutError as e:
    print(f"Timeout: {e}\n")
print(f"¿Está corriendo 2? {future.running()}")
print(f"¿Terminó? {future.done()}")

resultado = future.result() # Espera lo restante
print(f"¿Está corriendo 3? {future.running()}")
print(f"¿Terminó? {future.done()}")

print(f"Resultado: {resultado}")

executor.shutdown()