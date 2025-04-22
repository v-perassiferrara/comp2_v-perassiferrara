import os

fifo_write = "/tmp/chat2to1"
fifo_read = "/tmp/chat1to2"

if not os.path.exists(fifo_write):
    os.mkfifo(fifo_write)

if not os.path.exists(fifo_read):
    os.mkfifo(fifo_read)


# Leer respuesta
while True:
    try:
        fr = os.open(fifo_read, os.O_RDONLY | os.O_NONBLOCK)
    except Exception:
        continue

    respuesta = os.read(fr, 1024).decode().strip()
    print(f"User 1: {respuesta}")

    # Escribir respuesta
    fw = os.open(fifo_write, os.O_WRONLY | os.O_NONBLOCK)
    msg = input("User 2: ")
    msg = msg + '\n'
    os.write(fw,msg.encode())
