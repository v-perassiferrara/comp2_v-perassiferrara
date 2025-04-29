import signal, time

def handler_real(signum, frame):
    print("SIGALRM recibido")
    # dispara SIGALRM después de 5 segundos de tiempo real
    # (tiempo de reloj) (no de CPU) (periódicamente)
    signal.alarm(5)

def handler_virtual(signum, frame):
    print("SIGVTALRM recibido")
    

signal.signal(signal.SIGALRM, handler_real)
signal.signal(signal.SIGVTALRM, handler_virtual)


signal.alarm(5) # para iniciar la cadena de señales

# dispara SIGVTALRM después de 1 segundo de tiempo de CPU (no periódico)
signal.setitimer(signal.ITIMER_VIRTUAL, 1)

print("Esperando señales…")

try:
    while True:
        print("hola")
        for i in range(10**7):  # Proceso pesado para consumir CPU
            pass
        time.sleep(1) # bloquea hasta señal
        
except KeyboardInterrupt:
    print("Terminando.")