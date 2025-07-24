import json
import hashlib
import os
import datetime


BLOCKCHAIN_FILE = "blockchain.json"
REPORTE_FILE = "reporte.txt"



def verificar_integridad():
    
    if not os.path.exists(BLOCKCHAIN_FILE): # Verificar que la cadena existe
        print(f"Error: El archivo '{BLOCKCHAIN_FILE}' no fue encontrado.")
        exit(1)
        
    with open(BLOCKCHAIN_FILE, 'r') as f:
        try:
            blockchain = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: El archivo '{BLOCKCHAIN_FILE}' está corrupto o mal formado.")
            exit(1)

        if not blockchain:
            print("La cadena de bloques está vacía. No hay nada que verificar.")
            exit(1)

        print("--- Iniciando Verificación de Integridad de la Cadena ---")

        valid_blockchain = True # Inicialmente, asumimos que la cadena es válida
        
        # Para el primer bloque, usamos un hash génesis
        prev_hash_recalculado = hashlib.sha256('genesis'.encode()).hexdigest()
        

        # --- Verificación de cada bloque ---
        for i, block in enumerate(blockchain):
            print(f"Verificando Bloque {i}...")


            # Verificar el encadenamiento con el bloque previo
            if block['prev_hash'] != prev_hash_recalculado:
                print(f"  ERROR: Hash previo incorrecto en el bloque {i}!")
                print(f"     - Esperado: {prev_hash_recalculado[:10]}...")
                print(f"     - Encontrado: {block['prev_hash'][:10]}...")
                valid_blockchain = False
                break


            # Recalcular y verificar el hash del bloque actual
            prev_hash = block['prev_hash']
            data = block['datos']
            timestamp = block['timestamp']
            
            data_string = json.dumps(data, sort_keys=True)
                    
            raw_hash_string = prev_hash + timestamp + data_string
            
            hash_recalculado = hashlib.sha256(raw_hash_string.encode('utf-8')).hexdigest()
            
            if block['hash'] != hash_recalculado:
                print(f"  ERROR: Hash del bloque {i} corrupto. Los datos han sido modificados.")
                valid_blockchain = False
                break
            
                
            # Actualizar el hash para la siguiente iteración
            prev_hash_recalculado = block['hash']


    if valid_blockchain:
        print("\nVerificación completada. La cadena es VÁLIDA.\n")
    else:
        print("\nVerificación fallida. La cadena ha sido CORROMPIDA.\n")
        
    return blockchain if valid_blockchain else None



def generar_reporte(blockchain):
    '''
        Generar un reporte final (reporte.txt) con:
        - Cantidad total de bloques.
        - Número de bloques con alertas.
        - Promedio general de frecuencia, presión y oxígeno.
    '''
    
    total_blocks = len(blockchain)
    alert_blocks = 0
    
    sum_frecuencia = 0
    sum_presion = 0
    sum_oxigeno = 0
    
    for block in blockchain:
        sum_frecuencia += block['datos']['frecuencia']['media']
        sum_presion += block['datos']['presion']['media']
        sum_oxigeno += block['datos']['oxigeno']['media']
        
        if block['alerta']:
            alert_blocks += 1
            
    mean_frecuencia = sum_frecuencia / total_blocks
    mean_presion = sum_presion / total_blocks
    mean_oxigeno = sum_oxigeno / total_blocks
        
    with open(REPORTE_FILE, 'w') as f:
        f.write("--- Reporte de análisis biométrico ---\n\n")
        
        f.write("Fecha del reporte: " + datetime.datetime.now().isoformat(timespec='seconds') + "\n")
        
        f.write("\n")
        f.write(f"Total de bloques: {total_blocks}\n")
        f.write(f"Bloques con alerta: {alert_blocks}\n")
        f.write("\n")
        f.write(f"Promedio de frecuencia: {mean_frecuencia:.2f}\n")
        f.write(f"Promedio de presión (sistolica): {mean_presion:.2f}\n")
        f.write(f"Promedio de oxígeno: {mean_oxigeno:.2f}\n")
        f.write("------------------------------------------")


if __name__ == "__main__":
    cadena_verificada = verificar_integridad()
    if cadena_verificada:
        generar_reporte(cadena_verificada)
    else:
        print("No se generó un reporte porque la cadena es inválida o está vacía.")
        exit(1)