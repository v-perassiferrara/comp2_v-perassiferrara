import os

fifo_write = "/tmp/chat1to2"
fifo_read = "/tmp/chat2to1"

if not os.path.exists(fifo_write):
    os.mkfifo(fifo_write)

if not os.path.exists(fifo_read):
    os.mkfifo(fifo_read)


# Enviar mensaje
while True:
    try:
        fw = os.open(fifo_write, os.O_WRONLY | os.O_NONBLOCK)
    except Exception:
        continue
    
    msg = input("User 1: ")
    msg = msg + '\n'
    os.write(fw,msg.encode())

# Leer respuesta
while True:
    try:
        fr = os.open(fifo_read, os.O_RDONLY | os.O_NONBLOCK)
    except Exception:
        continue
    
    respuesta = os.read(fr, 1024).decode().strip()
    print(f"User 2: {respuesta}")
    
    
    
# Hacer una implementacion simple de chat donde el que comience a escribir pueda ser
# cualquiera (usando 2 fifos, bajo nivel) y no se bloquee innecesariamente