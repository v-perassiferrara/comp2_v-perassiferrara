import os

def comunicacion_pipe():
    # Creación del pipe
    r, w = os.pipe()

    pid = os.fork()
    if pid == 0:
        # Proceso hijo: cierra el extremo de escritura y lee
        os.close(w)
        r_end = os.fdopen(r)
        mensaje = r_end.read()
        print("Hijo recibió:", mensaje)
        r_end.close()
        os._exit(0)
    else:
        # Proceso padre: cierra el extremo de lectura y escribe
        os.close(r)
        w_end = os.fdopen(w, 'w')
        w_end.write("¡Hola desde el padre!\n")
        w_end.close()
        os.wait()  # Espera al hijo

if __name__ == '__main__':
    comunicacion_pipe()
