import os

pid = os.fork() # para el padre retorna el pid del hijo, para el hijo retorna 0
if pid == 0:
    print("[HIJO] PID:", os.getpid())
else:
    print("[PADRE] PID:", os.getpid(), "→ hijo:", pid)

