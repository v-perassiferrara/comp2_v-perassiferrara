"""
Ejercicio 9: Detección de procesos zombis en el sistema

Escribir un script que recorra el directorio /proc y detecte procesos
en estado zombi, listando su PID, PPID y el nombre del ejecutable.
Se debe realizar sin utilizar el comando 'ps'.

"""

import os

def detectar_zombis():

    for pid in os.listdir('/proc'): # Recorre cada elemento de /proc.

        if pid.isdigit():   # Se verifica que el elemento corresponda a un PID de proceso (es numerico).

            try:
                
                with open(f"/proc/{pid}/status") as f:  # Se abre el archivo status usando 'with' para asegurar que se cierre automáticamente.
                    lines = f.readlines()   # Se leen todas las líneas del archivo y se guardan en una lista.
                    
                    # Se utiliza una generator expression para obtener la primera línea que comience con "State:".
                    # La expresión "l for l in lines" significa: para cada línea 'l' en 'lines'
                    # y se filtra con "if l.startswith("State:")" para obtener solo la línea de estado.
                    # La función next() devuelve el primer elemento que cumpla la condición.
                    # Si no se encuentra ninguna, se retorna una cadena vacía ("").
                    estado = next((l for l in lines if l.startswith("State:")), "")
                    
                    if "Z" in estado: # se detecto estado zombi
                        # Se extrae el nombre del proceso buscando la línea que comienza con "Name:".
                        # Se utiliza split() para dividir la línea y se toma el segundo elemento,
                        # que corresponde al nombre del ejecutable.
                        nombre = next((l for l in lines if l.startswith("Name:")), "").split()[1]
                        
                        # Se extrae el PPID del proceso buscando la línea que comienza con "PPid:".
                        ppid = next((l for l in lines if l.startswith("PPid:")), "").split()[1]
                        
                        # Se imprime la información del proceso zombi detectado.
                        print(f"Zombi detectado → PID: {pid}, PPID: {ppid}, Nombre: {nombre}")

            except IOError:
                continue # Si ocurre un error al abrir o leer el archivo, se omite ese PID y se continúa con el siguiente

detectar_zombis()
