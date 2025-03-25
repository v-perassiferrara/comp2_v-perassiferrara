# Ejercicio 3: Ejecutar otro programa con exec()
# Objetivo: reemplazar el proceso hijo con un nuevo programa externo.

import os

pid_hijo = os.fork()

if pid_hijo == 0:
    print(os.getpid() , os.getppid())
    os.execlp("neofetch", "neofetch")
else:
    os.wait()