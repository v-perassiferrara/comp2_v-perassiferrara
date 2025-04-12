'''
Implementar un pipeline donde:

Proceso A genera números aleatorios

Proceso B filtra pares

Proceso C suma los resultados
'''




'''Mi versión original'''

# import os
# from random import randint


# def run_pipeline():
    
#     # Proceso 1
       
#     # Crea pipe 1-2 
#     r1, w1 = os.pipe()

#     pid = os.fork()
    

#     if pid == 0:    # Proceso 2
                
#         lista_pares = []
        
#         # Lee de pipe 1-2
#         os.close(w1)    # Cierra extremo de escritura 1
#         r_end1 = os.fdopen(r1)   # Abre el extremo de lectura 1
#         mensaje = r_end1.read()
#         print("Padre recibió:", mensaje)
#         for i in range(len(mensaje)):
#             numero = mensaje[i]
#             if int(numero) % 2 == 0:
#                 lista_pares.append(numero)
#         print("Lista de pares:", lista_pares)
#         r_end1.close()

#         # Crea pipe 2-3
#         r2, w2 = os.pipe()
        
#         pid2 = os.fork()
        
        
#         if pid2 == 0:   # Proceso 3
            
                    
#             # Lee de pipe 2-3
#             os.close(w2)    # Cierra extremo de escritura 2
#             r_end2 = os.fdopen(r2)  # Abre el extremo de lectura 2
#             mensaje = r_end2.read()
#             print("Hijo recibió:", mensaje)
#             total = 0
#             for numero in mensaje:
#                 total += int(numero)
#             print("Total:", total)
#             r_end2.close()
            
#             os._exit(0)
        
#         # Escribe 2 a 3
#         os.close(r2)    # Cierra el extremo de lectura 2
#         w_end2 = os.fdopen(w2, 'w') # Abre el extremo de escritura 2
#         for par in lista_pares:
#             w_end2.write(par)
#         w_end2.close()
        
#         os.waitpid(-1, 0)  # Espera al Proceso 3
#         os._exit(0)
    
#     lista_numeros = []
    
#     #Esribe 1 a 2
#     os.close(r1)   # Cierra el extremo de lectura 1
#     w_end1 = os.fdopen(w1, 'w') # Abre el extremo de escritura 1
#     for i in range(50):
#         lista_numeros.append(str(randint(0,9)))
#     print("Números generados:", lista_numeros)
#     w_end1.writelines(lista_numeros)
#     w_end1.close()

# if __name__ == "__main__":
#     run_pipeline()
#     os.waitpid(-1, 0) # Espera al proceso 1 y al proceso 2







'''Versión corregida y mejorada'''

import os
from random import randint

def run_pipeline():
    # Pipe A->B
    r_ab, w_ab = os.pipe()
    
    if os.fork() == 0:  # Proceso B
        os.close(w_ab)
        # Filtra pares
        with os.fdopen(r_ab) as f_ab:
            numeros = [int(line.strip()) for line in f_ab if line.strip()]
            pares = [str(n) for n in numeros if n % 2 == 0]
        
        # Pipe B->C
        r_bc, w_bc = os.pipe()
        if os.fork() == 0:  # Proceso C
            os.close(w_bc)
            with os.fdopen(r_bc) as f_bc:
                total = sum(int(line.strip()) for line in f_bc if line.strip())
                print(f"Suma total: {total}")
            os._exit(0)
        
        # Envía pares a C
        os.close(r_bc)
        with os.fdopen(w_bc, 'w') as f_bc:
            f_bc.write('\n'.join(pares) + '\n')
        
        os.waitpid(-1, 0)
        os._exit(0)
    
    # Proceso A
    os.close(r_ab)
    with os.fdopen(w_ab, 'w') as f_ab:
        numeros = [str(randint(0, 100)) for _ in range(50)]
        print(f"A generó: {numeros}")
        f_ab.write('\n'.join(numeros) + '\n')
    
    os.waitpid(-1, 0)

if __name__ == "__main__":
    run_pipeline()


'''
Mejoras clave:

- Formato de datos estructurado: Usa \n como separador

- Manejo seguro de líneas: strip() y verificación de líneas vacías

- Aleatoriedad real: Números entre 0-100 (más significativos)

- Legibilidad: Uso de list comprehensions y with    
'''