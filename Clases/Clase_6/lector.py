fifo = 'canal_fifo'

print("Abriendo FIFO para lectura…")
with open(fifo, 'r') as f:
    for linea in f:
        print(f"Recibido: {linea.strip()}")