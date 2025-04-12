'''
Ejercicio 1: Eco Simple
Crea un programa en Python que establezca comunicación entre un proceso padre y un hijo mediante un pipe.
El padre debe enviar un mensaje al hijo, y el hijo debe recibir ese mensaje y devolverlo al padre (eco).
'''

import os

def run_pipeline():
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
        w_end.write(mensaje)
        w_end.close()
        os._exit(0)

    else:
        # Proceso padre: cierra el extremo de lectura 1 y escribe
        os.close(r1)
        w_end = os.fdopen(w1, 'w')
        w_end.write("Mensaje del padre al hijo\n")
        w_end.close()
        
        # Proceso padre: cierra el extremo de escritura 2 y lee
        os.close(w2)
        r_end = os.fdopen(r2)
        mensaje = r_end.read()
        print("Padre recibió:", mensaje)
        r_end.close()
        os.wait()  # Espera al hijo



        

if __name__ == '__main__':
    run_pipeline()
