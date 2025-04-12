'''
Ejercicio 5: Chat Bidireccional
Desarrolla un sistema de chat simple entre dos procesos usando pipes.
Cada proceso debe poder enviar y recibir mensajes simultáneamente, implementando una comunicación bidireccional completa.
'''

# Mi versión, poco óptima y no simultánea


import os

def chat():
    # Creación del pipe
    r1, w1 = os.pipe()
    r2, w2 = os.pipe()

    pid = os.fork()
    if pid == 0:
        # Proceso hijo: cierra el extremo de escritura 1 y lee
        os.close(w1)
        r_end = os.fdopen(r1)
        mensaje = r_end.read()
        print("Hijo recibió:", mensaje)
        r_end.close()

        # Proceso hijo: cierra el extremo de lectura 2 y escribe
        os.close(r2)
        w_end = os.fdopen(w2, 'w')
        mensaje2 = str(input("Indicar mensaje de hijo al padre: ")) 
        w_end.write(mensaje2)
        w_end.close()
        os._exit(0)

    else:
        # Proceso padre: cierra el extremo de lectura 1 y escribe
        os.close(r1)
        w_end = os.fdopen(w1, 'w')
        mensaje1 = str(input("Indicar mensaje de padre al hijo: "))
        w_end.write(mensaje1)
        w_end.close()
        
        # Proceso padre: cierra el extremo de escritura 2 y lee
        os.close(w2)
        r_end = os.fdopen(r2)
        mensaje = r_end.read()
        print("Padre recibió:", mensaje)
        r_end.close()
        os.wait()  # Espera al hijo



        

if __name__ == '__main__':
    while True:
        chat()