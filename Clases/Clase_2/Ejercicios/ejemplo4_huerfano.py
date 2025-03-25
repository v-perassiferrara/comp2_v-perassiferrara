import os, time

pid = os.fork()
if pid > 0:
    print("[PADRE] Terminando rápidamente")
    os._exit(0)
else:
    print("[HIJO] Huérfano. Padre desaparecido. Mi nuevo padre será init.")
    time.sleep(10)  # Observar con `ps -o pid,ppid,stat,cmd`

'''
Lo que sucede es que el hijo que quedó huérfano pasa a tener un PPID de 1.
Es decir, que es "adoptado como hijo" por systemd/init, su nuevo proceso padre.
'''