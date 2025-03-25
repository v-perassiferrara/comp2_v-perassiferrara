# Simula un servidor que atiende conexiones de clientes (ficticios) lanzando un hijo por cada uno.
# Ideal para comprender cómo escalar procesos de manera controlada.

import os, time

def atender_cliente(n):
    pid = os.fork()
    if pid == 0:
        print(f"Atendiendo Cliente {(n+1)}")
        time.sleep(2)
        print(f"Cliente {(n+1)} atendido con éxito")
        os._exit(0)

n = 5

print(f"Padre {os.getpid()}")

for cliente in range(n):
    atender_cliente(cliente)
    time.sleep(3)

for j in range(n):
    os.wait()



