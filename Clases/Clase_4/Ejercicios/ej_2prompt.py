'''
Ejercicio 1: Pipeline Simple
Objetivo: Crear un pipeline de tres procesos donde el primer proceso genera datos,
el segundo modifica esos datos y el tercero los muestra en pantalla.

Pistas para la implementación:

Crea dos pipes: uno para la comunicación del proceso 1 al 2 y otro del proceso 2 al 3.

Usa os.fork() en cadena para crear los procesos.

Asegúrate de cerrar los extremos de los pipes que no serán utilizados en cada proceso.
'''

import os


def run_pipeline():
    
    # Proceso 1
    
    print("Proceso 1\n")
   
    # Crea pipe 1-2 
    r1, w1 = os.pipe()

    pid = os.fork()
    

    if pid == 0:    # Proceso 2
        
        print("Proceso 2\n")
        
        # Lee de pipe 1-2
        os.close(w1)    # Cierra extremo de escritura 1
        r_end1 = os.fdopen(r1)   # Abre el extremo de lectura 1
        mensaje = r_end1.read()
        print("Hijo recibió:", mensaje)
        r_end1.close()

        # Crea pipe 2-3
        r2, w2 = os.pipe()
        
        pid2 = os.fork()
        
        
        if pid2 == 0:   # Proceso 3
            
            
            print("Proceso 3\n")
            
            # Lee de pipe 2-3
            os.close(w2)    # Cierra extremo de escritura 2
            r_end2 = os.fdopen(r2)  # Abre el extremo de lectura 2
            mensaje = r_end2.read()
            print("Hijo recibió:", mensaje)
            r_end2.close()
            
            os._exit(0)
        
        # Escribe 2 a 3
        os.close(r2)    # Cierra el extremo de lectura 2
        w_end2 = os.fdopen(w2, 'w') # Abre el extremo de escritura 2
        w_end2.write("¡Hola desde el proceso 2!\n")
        w_end2.close()
        
        os.waitpid(-1, 0)  # Espera al Proceso 3
        os._exit(0)
    
    #Esribe 1 a 2
    os.close(r1)   # Cierra el extremo de lectura 1
    w_end1 = os.fdopen(w1, 'w') # Abre el extremo de escritura 1
    w_end1.write("¡Hola desde el proceso 1!\n")
    w_end1.close()

if __name__ == "__main__":
    run_pipeline()
    os.waitpid(-1, 0) # Espera al proceso 1 y al proceso 2