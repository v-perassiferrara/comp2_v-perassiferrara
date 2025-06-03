# ver como se ven los file descriptors indicando que pasa con ls -l con la clase pipe de multiprocessing (no os.pipe)

from multiprocessing import Process, Pipe
import os
import time

def tarea(conn):
    conn.send("Hola desde hijo")
    print("Hijo empezó")
    time.sleep(10)
    print("Hijo terminando")

if __name__ == "__main__":
    print(os.getpid())
    padre_conn, hijo_conn = Pipe()
    p = Process(target=tarea, args=(hijo_conn,))
    p.start()
    print(padre_conn.recv())
    p.join()
    
