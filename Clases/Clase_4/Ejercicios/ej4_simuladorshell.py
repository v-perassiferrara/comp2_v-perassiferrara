'''
Ejercicio 4: Simulador de Shell
Implementa un programa que simule una versión simplificada del operador pipe (|) de la shell.
El programa debe ejecutar dos comandos proporcionados por el usuario y conectar la salida del primero con la entrada del segundo.
'''

import os, sys


def simulate_pipe(cmd1,cmd2):
    
    # Crea pipe 1-2 
    r, w = os.pipe()

    pid = os.fork()

    if pid == 0:  # Comando 2
        
        os.close(w)  # Cierra extremo de escritura
        os.dup2(r, sys.stdin.fileno())  # Redirige standard input al pipe (toma datos del pipe)
        os.execvp(cmd2.split()[0], cmd2.split())
        os.close(r)  # Cierra el descriptor original ahora que está duplicado
        os._exit(0)
        
        
    # Comando 1
    
    os.close(r)   # Cierra el extremo de lectura
    os.dup2(w, sys.stdout.fileno())  # Redirige standard output al descriptor del pipe
    os.close(w)  # Cerramos el descriptor original ahora que está duplicado
    os.execvp(cmd1.split()[0], cmd1.split())  # Corre el primer comando
        
    os.wait()  # Espera al Proceso 2



def main():
    
    while True:
        entrada = input("\n$ ")
        cmd1, cmd2 = [cmd.strip() for cmd in entrada.split("|")]
        simulate_pipe(cmd1,cmd2)



if __name__ == "__main__":
    main()