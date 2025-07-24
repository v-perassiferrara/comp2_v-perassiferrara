import os
import multiprocessing
import datetime
import queue
import hashlib
import json
import random
import time


def generator(pipes):
    
    print("[Generador] Simulación iniciada.")
    
    for _ in range(60):
        data = {
        "timestamp": datetime.datetime.now().isoformat(timespec='seconds'),
        "frecuencia": random.randint(60,180),
        "presion": [random.randint(110,180), random.randint(70,110)],
        "oxigeno": random.randint(90,100)
        }
        
        # Enviamos el mismo dato a cada analizador
        for conn in pipes:
            conn.send(data)

        time.sleep(1)
    
    # Cierra los extremos de escritura de los pipes para señalar el fin de datos
    for conn in pipes:
        conn.close()
    print("[Generador] Simulación finalizada. Todos los datos enviados.")


def analyzer(variable, child_conn, queue_to_verifier):

    # Diccionario para almacenar las listas de valores de la ventana.
    # Ej: {'sistolica': [dato1, dato2, ...], 'oxigeno': [dato1, dato2, ...], ...}
    analyzed_series_data = {} 
    

    
    while True:
        try:
            data = child_conn.recv() # Recibimos el dato del generador
            raw_value = data[variable] # Valor crudo: único o lista de 2 valores (presión)
            timestamp_original = data["timestamp"]             
                        
            if variable == "presion": # Para presión, consideramos solo la sistólica
                values_to_process = [("sistolica", raw_value[0])] # Solo la sistólica (primer valor)
            else: # Para frecuencia y oxígeno, solo hay un valor
                values_to_process = [(variable, raw_value)]


            # Procesamos cada valor
            for series_name, value_to_add in values_to_process:
                
                # Si no existe la lista para la serie, la creamos
                if series_name not in analyzed_series_data:
                    analyzed_series_data[series_name] = []
                
                # Mantener la ventana móvil de los últimos 30 valores
                current_list = analyzed_series_data[series_name] # Lista actual para la serie respectiva

                if len(current_list) >= 30: 
                    current_list.pop(0) # Eliminar el más antiguo

                current_list.append(value_to_add) # Agregar el nuevo valor
            
            
            # Para cada serie correspondiente, calcular las estadísticas y mostrarlas
            for series_name, current_list in analyzed_series_data.items():
                if len(current_list) > 0: # Verificar que la lista no esté vacía
                    
                    mean = sum(current_list) / len(current_list)
                    var = sum((x - mean) ** 2 for x in current_list) / len(current_list)
                    stdev = (var) ** 0.5

                    stats_packet = {
                        "tipo": series_name,
                        "timestamp": timestamp_original,
                        "media": round(mean, 2),
                        "desv": round(stdev, 2)
                    }
                    
                    queue_to_verifier.put(stats_packet) # Enviar el paquete a la cola hacia el verificador
            
            time.sleep(1)
            
        except EOFError:
            print(f"[{variable.capitalize()}] Generador ha terminado. Saliendo.")
            queue_to_verifier.put(None)
            break
        except Exception as e:
            print(f"[{variable.capitalize()}] Error: {e}")
            queue_to_verifier.put(None)
            break
        
    os._exit(0)


def verifier(queue_from_analyzers):
      
    blockchain = []
    # Cargar blockchain existente si existe
    if os.path.exists("blockchain.json"):
        with open("blockchain.json", 'r') as f:
            try:
                blockchain = json.load(f)
            except json.JSONDecodeError:
                print("[Verificador] 'blockchain.json' está vacío o corrupto. Se creará uno nuevo.")
    
    # Obtener el hash del último bloque o crear un hash génesis
    prev_hash = blockchain[-1]['hash'] if blockchain else hashlib.sha256('genesis'.encode()).hexdigest()
      
    
    finished_analyzers = 0 # Contador para saber cuántos analizadores han terminado
    
    num_analyzers = 3 # Hay 3 analizadores en total (A, B, C)
    
    pending = {} # Diccionario para almacenar los paquetes por timestamp


    while finished_analyzers < num_analyzers: # Mientras no hayan terminado todos los analizadores
        try:
            packet = queue_from_analyzers.get(timeout=2) # Recibimos el paquete de estadísticas (diccionario)
            
            if packet is None: # Si recibimos None, significa que un analizador ha terminado
                finished_analyzers += 1
                continue
            
            # Procesar el paquete de estadísticas
            timestamp = packet["timestamp"]
            data_type = packet["tipo"]
                
            # Agrupar los paquetes por timestamp
            if timestamp not in pending:
                pending[timestamp] = {}
            pending[timestamp][data_type] = {
                "media": packet["media"],
                "desv": packet["desv"]
            }         
            
            # Comprobar si un timestamp está completo
            expected_keys = {"frecuencia", "sistolica", "oxigeno"} 

            if expected_keys.issubset(pending[timestamp].keys()):
                # Si tenemos todos los datos para un timestamp, procesamos el bloque 
                
                
                
                # --- Comprobación de rangos y alerta ---
                alert = False
                
                mean_frecuencia = pending[timestamp]["frecuencia"]["media"]
                mean_sistolica = pending[timestamp]["sistolica"]["media"]
                mean_oxigeno = pending[timestamp]["oxigeno"]["media"]
                
                if mean_frecuencia >= 200 or not (90 <= mean_oxigeno <= 100) or mean_sistolica >= 200:
                    alert = True   # Si alguno de los datos está fuera de rango, se marca el bloque con alerta
                
                
                
                # --- Cálculo del hash y construcción del bloque ---
                block_data = {
                    "frecuencia": pending[timestamp]["frecuencia"],
                    "presion": pending[timestamp]["sistolica"], # Consideramos solo la sistólica
                    "oxigeno": pending[timestamp]["oxigeno"]
                }
                
                
                # Para asegurar el mismo orden siempre, usamos json.dumps con sort_keys
                data_string = json.dumps(block_data, sort_keys=True)
                
                # Concatenamos los elementos para el hash:
                raw_hash_string = prev_hash + timestamp + data_string
                
                # Calculamos el hash
                current_hash = hashlib.sha256(raw_hash_string.encode('utf-8')).hexdigest()


                block = {
                    "timestamp": timestamp,
                    "datos": block_data,
                    "alerta": alert,
                    "prev_hash": prev_hash,
                    "hash": current_hash
                }
                
                
                # Agregamos el bloque a la blockchain
                blockchain.append(block)
                
                # Persistimos el bloque en blockchain.json
                try:
                    with open("blockchain.json", 'w') as f:
                        json.dump(blockchain, f, indent=4) # indent=4 para que el JSON sea legible, identa 4 espacios en cada nivel
                    print(f"[BLOQUE {len(blockchain) - 1}] Hash: {current_hash} | Alerta: {alert}")
                except Exception as file_e:
                    print(f"[VERIFICADOR] Error al escribir en blockchain.json: {file_e}")
                
                
                # Actualizamos el hash previo para procesar el siguiente bloque
                prev_hash = current_hash
                
                
                # Eliminamos el timestamp de pending para no procesarlo de nuevo
                del pending[timestamp] # Importante para liberar la entrada una vez procesada
            
                
        except Exception as e:
            print(f"[VERIFICADOR] Error al recibir de la cola: {e}")
            break
        
    print("[VERIFICADOR] Todos los analizadores han terminado y sus señales de fin recibidas. Saliendo.")
    os._exit(0)
        

if __name__ == "__main__":
    
    # Creamos el archivo de blockchain
    if not os.path.exists("blockchain.json"):
        with open("blockchain.json", 'w') as f:
            json.dump([], f)
    
    # Creamos los pipes generador-analizador
    parent_A, child_A = multiprocessing.Pipe()
    parent_B, child_B = multiprocessing.Pipe()
    parent_C, child_C = multiprocessing.Pipe()

    # Creamos una única Queue para que los analizadores envíen sus resultados al verificador
    queue_for_verifier = multiprocessing.Queue()

    # Creamos los procesos analizadores A, B, C
    proc_A = multiprocessing.Process(target=analyzer, args=("frecuencia", child_A, queue_for_verifier))
    proc_B = multiprocessing.Process(target=analyzer, args=("presion", child_B, queue_for_verifier))
    proc_C = multiprocessing.Process(target=analyzer, args=("oxigeno", child_C, queue_for_verifier))

    # Creamos el proceso verificador
    proc_verifier = multiprocessing.Process(target=verifier, args=(queue_for_verifier,))


    # Iniciamos los procesos
    proc_A.start()
    proc_B.start()
    proc_C.start()
    
    proc_verifier.start()


    # Corremos el generador
    generator([parent_A, parent_B, parent_C])


    # Cerramos los extremos de escritura para que los analizadores terminen cuando el generador termine
    parent_A.close()
    parent_B.close()
    parent_C.close()

    proc_A.join()
    proc_B.join()
    proc_C.join()
        
    proc_verifier.join()

    print("Todos los procesos (Generador, Analizadores y Verificador) han terminado.")