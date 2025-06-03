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