'''
Ejercicio 2: Contador de Palabras
Implementa un sistema donde el proceso padre lee un archivo de texto y envía su contenido línea por línea a un proceso hijo a través de un pipe.
El hijo debe contar las palabras en cada línea y devolver el resultado al padre.
'''

import os

def run_pipeline():
    # Creación del pipe
    r1, w1 = os.pipe()
    r2, w2 = os.pipe()
    ruta_archivo = "comp2_v-perassiferrara/Clases/Clase_4/Ejercicios/archivo_random.txt"

    pid = os.fork()
    if pid == 0:
        # Proceso hijo: cierra el extremo de escritura 1 y lee
        os.close(w1)
        with os.fdopen(r1) as r1_end:   
            mensaje = r1_end.read()     # El hijo recibe el mensaje del padre
            numero_linea = 0    # Contador de lineas
            resultado = ""  # String para guardar el resultado
            for line in mensaje.splitlines(): # El hijo lee cada linea del mensaje
                palabras = line.replace(',', ' ').split() # Dividimos la linea en palabras
                numero_palabras = len(palabras) # Contamos el número de palabras
                resultado += f"Línea {numero_linea+1} tiene {numero_palabras} palabras\n"
                numero_linea += 1

        # Proceso hijo: cierra el extremo de lectura 2 y escribe
        os.close(r2)
        with os.fdopen(w2, 'w') as w2_end:
            w2_end.write(resultado)
        os._exit(0)

    else:
        # Proceso padre: cierra el extremo de lectura 1 y escribe
        os.close(r1)
        with os.fdopen(w1, 'w') as w1_end:
            with open(ruta_archivo, 'r') as archivo: # El padre lee un archivo
                for line in archivo:    # Lee cada linea del archivo
                    w1_end.write(line)  # Y la env a al hijo por el pipe 1
        
        # Proceso padre: cierra el extremo de escritura 2 y lee
        os.close(w2)
        with os.fdopen(r2) as r2_end:
            mensaje = r2_end.read()
            print(f"\nPadre recibió: \n\n{mensaje}")
        os.wait()  # Espera al hijo



if __name__ == '__main__':
    run_pipeline()

