import os, time, sys

def main():
    r_padre_a_hijo, w_padre_a_hijo = os.pipe()
    
    pid = os.fork()

    if pid > 0:  # Proceso padre  
            
        os.close(r_padre_a_hijo)    
    
        os.write(w_padre_a_hijo, b"Hola hijo\n")
        
        print(os.getpid())
        
        time.sleep(30)
        
        os.close(w_padre_a_hijo)
        
        
    else:  # Proceso hijo
        os.close(w_padre_a_hijo)
        
        mensaje = os.read(r_padre_a_hijo, 1024)
        time.sleep(30)
        os.close(r_padre_a_hijo)
        
        os._exit(0)

if __name__ == "__main__":
    main()
    
'''

genera:

$ ls -l /proc/44468/fd
total 0
lrwx------. 1 valen valen 64 may  6 11:04 0 -> /dev/pts/2
lrwx------. 1 valen valen 64 may  6 11:04 1 -> /dev/pts/2
lr-x------. 1 valen valen 64 may  6 11:04 103 -> /usr/share/code/v8_context_snapshot.bin
lrwx------. 1 valen valen 64 may  6 11:04 2 -> /dev/pts/2
l-wx------. 1 valen valen 64 may  6 11:04 37 -> /home/valen/.config/Code/logs/20250506T090203/ptyhost.log
lrwx------. 1 valen valen 64 may  6 11:04 38 -> /dev/ptmx
l-wx------. 1 valen valen 64 may  6 11:04 4 -> 'pipe:[506511]'


'''