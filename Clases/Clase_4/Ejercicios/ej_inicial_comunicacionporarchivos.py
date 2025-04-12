# Hacer que dos procesos se comuniquen entre sí mediante archivos, encontrar limitaciones?

import os, time

def crear_hijos():

    archivo = open("Clases/Clase_3/Ejercicios/archivo_compartido.txt", "w")    
    archivo.write("Soy el abuelo\n")

    for i in range(5): # Crea 5 padres
        pid = os.fork()
        if pid == 0:

            archivo.write(f"Soy el padre {i}\n")

            pid2 = os.fork() # Crea un hijo para cada padre

            if pid2 == 0:
                archivo.write(f"Soy el hijo del padre {i}\n")
                archivo.close()
                os._exit(0)

            os.wait()
            archivo.close()
            os._exit(0)

    archivo.close()

    archivo = open("Clases/Clase_3/Ejercicios/archivo_compartido.txt", "r")
    print(archivo.read())
    archivo.close()

if __name__ == "__main__":
    crear_hijos()
    os.wait()
    
'''

Como limitaciones:
- Varios procesos podrían intentar escribir a la vez y sobreescribir el contenido de la misma línea.
- Los procesos heredan el descriptor del archivo abierto, causando escrituras duplicadas o corrupción.
- El orden de ejecución es no determinista, generando salidas caóticas.
- Cierre inseguro del archivo por múltiples procesos simultáneamente.
- El "abuelo" podría leer el archivo antes de que todos los hijos terminen de escribir.

'''