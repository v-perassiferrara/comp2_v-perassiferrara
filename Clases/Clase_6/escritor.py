import os
import time

fifo = 'canal_fifo'
# Asegurarse de que exista
try:
    os.mkfifo(fifo)
except FileExistsError:
    pass

print("Abriendo FIFO para escritura…")
with open(fifo, 'w') as f:
    for i in range(5):
        msg = f"Mensaje {i}\n"
        f.write(msg)
        f.flush()
        print(f"Enviado: {msg.strip()}")
        time.sleep(1)