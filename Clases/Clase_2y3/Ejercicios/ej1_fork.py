# Ejercicio 1: Crear un proceso hijo y mostrar los PID
# Objetivo: utilizar fork() y comprender la relación padre-hijo.

import os


pid_hijo = os.fork()

if pid_hijo == 0:
    print("Hijo: ", os.getpid())
else:
    print("Padre: ", os.getpid())