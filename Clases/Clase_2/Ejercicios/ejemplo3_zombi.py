import os, time

pid = os.fork()
if pid == 0:
    print("[HIJO] Terminando")
    os._exit(0)
else:
    print("[PADRE] Esperando sin recolectar al hijo")
    time.sleep(15)  # Tiempo suficiente para observar al zombi con `ps`


'''
Durante esos 15 segundos, el proceso hijo aparecerá en el sistema como un zombi.
Puede observarse con: ps -el | grep Z
'''