from concurrent.futures import ThreadPoolExecutor
import time
import random

def tarea(id):
    """Tarea que tarda tiempo variable"""
    duracion = random.uniform(1, 3)
    time.sleep(duracion)
    
    # Simular fallo ocasional
    if random.random() < 0.2:
        raise Exception(f"Tarea {id} falló")
    
    return {"id": id, "duracion": duracion}

def on_tarea_completa(future):
    """Callback ejecutado cuando una tarea termina"""
    try:
        resultado = future.result()
        print(f"✓ Tarea {resultado['id']} completada en {resultado['duracion']:.2f}s")
        
        # Aquí podrías hacer algo útil: guardar en DB, notificar, etc.
        
    except Exception as e:
        print(f"✗ Tarea falló: {e}")

def pool_con_callbacks(num_tareas):
    """Executor con callbacks para no bloquear"""
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Enviar tareas con callback
        for i in range(num_tareas):
            future = executor.submit(tarea, i)
            # add_done_callback() se ejecuta cuando termina
            future.add_done_callback(on_tarea_completa)
        
        # El executor espera a todas en el __exit__
        print("Tareas enviadas, esperando...")
    
    print("\n✓ Todas las tareas procesadas")

# Uso
if __name__ == "__main__":
    pool_con_callbacks(num_tareas=10)