import os

pid = os.fork()
if pid == 0:
    os.execlp("ls", "ls", "-l") # Solo se ejecuta en el hijo (indica ejecutable, nombre de programa y parametro -l)
else:
    os.wait()  # El padre espera que el hijo termine (debe hacerlo para evitar procesos zombi)