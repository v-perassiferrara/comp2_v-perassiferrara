from multiprocessing import Lock

lock = Lock()

with lock:
    # zona crítica segura
    a = 1
    print(a)