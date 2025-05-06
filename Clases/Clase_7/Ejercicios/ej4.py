
'''
Ejercicio 4: Control multihilo con señales externas
Objetivo: Integrar señales con hilos y control de ejecución.

Enunciado: Crea un programa multihilo donde un hilo cuenta regresivamente desde 30.
Usa una variable global con threading.Lock() para permitir que otro proceso externo,
al enviar una señal (SIGUSR1), pause la cuenta y otra señal (SIGUSR2) la reinicie.
El hilo principal debe instalar los handlers y proteger correctamente el estado compartido.
'''

# SOLUCION GENERADA POR IA DADO QUE NO HEMOS VISTO HILOS/THREADING TODAVIA

'''
Importantes:
- Usamos threading.Lock() para garantizar que no haya condiciones de carrera al leer o modificar pausado.

- Este patrón es esencial en sistemas concurrentes donde hay eventos externos (señales)
que modifican el flujo de ejecución.

- El hilo nunca termina abruptamente: la señal no interrumpe directamente al hilo,
sino que modifica un estado compartido.
'''




import threading
import signal
import time
import os

# Estado global que controla si la cuenta está pausada
pausado = False
lock = threading.Lock()

def handler(signum, frame):
    global pausado
    with lock:
        if signum == signal.SIGUSR1:
            pausado = True
            print("[SIGNAL] Pausando la cuenta (SIGUSR1)")
        elif signum == signal.SIGUSR2:
            pausado = False
            print("[SIGNAL] Reanudando la cuenta (SIGUSR2)")

# Asociar las señales a un único handler
signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGUSR2, handler)

def cuenta_regresiva():
    for i in range(30, 0, -1):
        with lock:
            if pausado:
                print(f"[PAUSADO] Esperando... ({i})")
            else:
                print(f"[ACTIVO] Cuenta regresiva: {i}")
        
        time.sleep(1)

        # Si está pausado, esperamos en bucle hasta que se reanude
        while True:
            with lock:
                if not pausado:
                    break
            time.sleep(0.5)

# Mostrar PID para que puedas enviar señales externas con kill -SIGUSR1/-SIGUSR2
print("PID:", os.getpid())
print("Enviá SIGUSR1 para pausar o SIGUSR2 para reanudar la cuenta.")

# Crear y lanzar el hilo
hilo = threading.Thread(target=cuenta_regresiva)
hilo.start()

# Esperar que el hilo termine
hilo.join()
print("Cuenta finalizada.")

