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
    
    print("Proceso 1")
   
    # Crea pipe 1-2 
    r1, w1 = os.pipe()
    
    #Esribe 1 a 2
    os.close(r1)
    w_end1 = os.fdopen(w1, 'w')
    w_end1.write("¡Hola desde el proceso 1!\n")
    w_end1.close()
    
    
    pid = os.fork()
    
    
    if pid == 0:
        
        print("Proceso 2")
        
        # Lee de pipe 1-2
        os.close(w1)
        r_end1 = os.fdopen(r1)
        mensaje = r_end1.read()
        print("Hijo recibió:", mensaje)
        r_end1.close()

        # Crea pipe 2-3
        r2, w2 = os.pipe()
        
        # Escribe 2 a 3
        os.close(r2)
        w_end2 = os.fdopen(w2, 'w')
        w_end2.write("¡Hola desde el proceso 1!\n")
        w_end2.close()
        
        
        pid2 = os.fork()
        
        
        if pid2 == 0:
            
            
            print("Proceso 3")
            
            # Lee de pipe 2-3
            os.close(w2)
            r_end2 = os.fdopen(r2)
            mensaje = r_end2.read()
            print("Hijo recibió:", mensaje)
            r_end2.close()
            
            os._exit(0)
        
        os.wait()
        os._exit(0)
    

if __name__ == "__main__":
    run_pipeline()
    os.wait()