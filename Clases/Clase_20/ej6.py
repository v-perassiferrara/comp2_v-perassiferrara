def tarea_numeros():
    """Cuenta números del 1 al 5, despacio"""
    for i in range(1, 6):
        print(f"  [Números] Contando: {i}")
        yield  # "He hecho mi parte, ahora le toca a otro"

def tarea_letras():
    """Genera letras de A a E, despacio"""
    for letra in 'ABCDE':
        print(f"  [Letras] Generando: {letra}")
        yield

# El "scheduler" más simple del mundo
def scheduler(tareas):
    """Ejecuta tareas en round-robin"""
    while tareas:
        for tarea in tareas[:]:  # Copia para modificar durante iteración
            try:
                next(tarea) # ejecutar la "ronda" de la tarea
            except StopIteration:
                tareas.remove(tarea)  # Tarea terminada, la quitamos

# Crear las tareas
t1 = tarea_numeros()
t2 = tarea_letras()

print("Ejecutando tareas de forma cooperativa:\n")
scheduler([t1, t2]) # va iterando por las tareas (primero una y luego la otra)