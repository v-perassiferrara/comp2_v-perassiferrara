'''
Ejercicio 3: Pipeline de Filtrado
Crea una cadena de tres procesos conectados por pipes donde: el primer proceso genera números aleatorios entre 1 y 100,
el segundo proceso filtra solo los números pares, y el tercer proceso calcula el cuadrado de estos números pares.
'''

import os
from random import randint

def run_pipeline():
    
    # Pipe 1->2
    r_12, w_12 = os.pipe()
    
    if os.fork() == 0:  # Proceso 2
        
        os.close(w_12)
        with os.fdopen(r_12) as r_12:
            
            numeros = [] # Crea una lista vacía para los números
            for line in r_12:
                line = line.strip() # Toma cada línea y elimina los espacios en blanco
                if line:    
                    numeros.append(int(line))   # Si la línea no está vacía, añade el número a la lista
                    
            pares = []  # Crea una lista vacía para los pares
            for n in numeros:
                if n % 2 == 0:
                    pares.append(str(n))    # Añade el número a la lista si es par
    
            print(f"\nProceso 2 filtró a: {pares}") 

        
        # Pipe 2->3
        
        r_23, w_23 = os.pipe()
        
        if os.fork() == 0:  # Proceso 3
            
            os.close(w_23)
            
            with os.fdopen(r_23) as r_23:
                
                cuadrados = []  # Crea una lista vacía para los cuadrados
                for line in r_23:
                    line = line.strip() # Toma cada línea y elimina los espacios en blanco
                    if line:    
                        cuadrados.append(int(line)**2)  # Si la línea no está vacía, añade su cuadrado a la lista
                        
                print(f"\nCuadrados de los pares: {cuadrados}")
                
            os._exit(0)
        
        
        
        # Envía pares a 3
        
        os.close(r_23)
        with os.fdopen(w_23, 'w') as w_23:
            w_23.write('\n'.join(pares))
        
        os.wait()
        os._exit(0)
    
    
    
    # Proceso 1
    
    os.close(r_12)
    with os.fdopen(w_12, 'w') as w_12:
        
        numeros = []
        for i in range(50):
            numeros.append(str(randint(0, 100)))
            
        print(f"\nProceso 1 generó: {numeros}")
        
        w_12.write('\n'.join(numeros))  # Une los números en un string (separados por \n) y los envía por el pipe
    
    os.wait()

if __name__ == "__main__":
    run_pipeline()