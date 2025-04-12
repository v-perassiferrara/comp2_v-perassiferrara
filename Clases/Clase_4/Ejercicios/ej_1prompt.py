# Modifica el código para enviar 10 números del padre al hijo

import os

def main():
    r, w = os.pipe()
    pid = os.fork()

    if pid > 0:  # Proceso padre      
        os.close(r)    # Cierra extremo de lectura
        w_end = os.fdopen(w,"w")   # Abre el extremo de escritura
        for i in range(10):
            w_end.write(f"{i}\n")
        w_end.close()
        os.wait()
        
        
    else:  # Proceso hijo
        os.close(w)    # Cierra extremo de escritura
        r_end = os.fdopen(r)   # Abre el extremo de lectura
        mensaje = r_end.read()
        print(mensaje)
        r_end.close()

if __name__ == "__main__":
    main()