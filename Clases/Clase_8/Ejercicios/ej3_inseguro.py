'''
Ejercicio 3 · Nivel Intermedio +
Objetivo: demostrar una condición de carrera y su corrección con Lock.

Enunciado: crea un contador global al que dos procesos suman 1, cincuenta mil veces cada uno.
Realiza primero la versión sin Lock (para evidenciar valores erróneos) y luego protégela con un Lock,
mostrando el resultado correcto (100.000).
'''

from multiprocessing import Process, Value

contador = Value('i', 0) # crea un contador compartido global entero

def incrementar(variable):
    for _ in range(50000):
        variable.value += 1
        
if __name__ == '__main__':
    # Sin Lock
    p1 = Process(target=incrementar, args=(contador,))
    p2 = Process(target=incrementar, args=(contador,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("Sin locks:", contador.value)
    print("Debería ser 100000")

# Comentario: Value permite memoria compartida; el Lock garantiza atomicidad.