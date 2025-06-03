from multiprocessing import Process, Lock, Value

contador = Value('i', 0) # crea un contador compartido global entero

def incrementar(variable, lock):
    for _ in range(50000):
        with lock: # bloquea el acceso a la variable
            variable.value += 1
        
if __name__ == '__main__':
    # Con Lock
    
    lock = Lock()
    
    p1 = Process(target=incrementar, args=(contador, lock))
    p2 = Process(target=incrementar, args=(contador, lock))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("Con locks:", contador.value)
    print("Debería ser 100000")