
'''
Enunciado: Diseñar un demonio de log centralizado que filtre mensajes
según prioridad usando un FIFO por nivel de log.
Implementar un multiplexor de FIFOs usando select().


Solución generada por IA

'''

import os, sys, errno, select, time

FIFO_DIR    = '/tmp'
LEVELS      = ['DEBUG','INFO','WARN','ERROR']
FIFO_PATHS  = { lvl: os.path.join(FIFO_DIR, f'log_{lvl}') for lvl in LEVELS }
LOG_DIR     = os.path.join(os.getcwd(), 'daemon_log/logs')

GLOBAL_LOG  = os.path.join(LOG_DIR, 'all.log')
LEVEL_FILES = { lvl: os.path.join(LOG_DIR, lvl.lower()+'.log') for lvl in LEVELS }

def daemonize():
    """Convertir el proceso actual en daemon (doble fork).

    Un daemon es un proceso que no tiene controlador de terminal asociado.
    Para lograr esto, debemos:

    1. Crear un proceso hijo (primer fork). El proceso original muere.
    2. En el proceso hijo, crear otro proceso hijo (segundo fork). El
       proceso que llam  al segundo fork se convierte en init (proceso
       raiz) y se encarga de los procesos zombies.
    3. En el proceso nuevo, cambiar el directorio de trabajo al raiz
       (no queremos que el proceso dependa de un directorio de trabajo
       particular).
    4. Cambiar la umask a 0 para que los archivos generados tengan
       permisos 666 y no dependan de la umask del usuario que lo llama.
    5. Redirigir la entrada, salida y error estandar a /dev/null para
       que el proceso no tenga controlador de terminal asociado.
    """

    if os.fork() > 0:
        sys.exit(0)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    if os.fork() > 0:
        sys.exit(0)
    # Redirigir stdio a /dev/null
    devnull = open('/dev/null','rb')
    os.dup2(devnull.fileno(), sys.stdin.fileno())
    devnull = open('/dev/null','ab')
    os.dup2(devnull.fileno(), sys.stdout.fileno())
    os.dup2(devnull.fileno(), sys.stderr.fileno())

def ensure_fifos():
    """Crear los FIFOs si no existen."""
    for path in FIFO_PATHS.values():
        try:
            if not os.path.exists(path):
                os.mkfifo(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

def ensure_logs():
    """Crear directorio de logs y archivos iniciales."""
    os.makedirs(LOG_DIR, exist_ok=True)
    open(GLOBAL_LOG, 'a').close()
    for f in LEVEL_FILES.values():
        open(f, 'a').close()

def open_fifos():
    """Abrir todos los FIFOs en modo no bloqueante y retornarlos."""
    fds = {}
    for lvl, path in FIFO_PATHS.items():
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
        fds[fd] = lvl
    return fds

def route_message(level, message):
    """Escribir el mensaje en el log global y en el log de nivel."""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{timestamp}] {level}: {message}\n'
    # Log global
    with open(GLOBAL_LOG, 'a') as gf:
        gf.write(line)
    # Log por nivel
    with open(LEVEL_FILES[level], 'a') as lf:
        lf.write(line)

def run():
    daemonize()
    ensure_fifos()
    ensure_logs()
    fds = open_fifos()
    poller = select.poll()
    for fd in fds:
        poller.register(fd, select.POLLIN)
    # Bucle principal
    while True:
        events = poller.poll()  # bloqueante hasta que haya datos
        for fd, _ in events:
            lvl = fds[fd]
            try:
                data = os.read(fd, 4096).decode().strip()
            except OSError:
                continue
            if data:
                for line in data.splitlines():
                    route_message(lvl, line)

if __name__ == '__main__':
    print(os.getcwd())
    run()