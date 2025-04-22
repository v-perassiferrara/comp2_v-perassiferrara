import os

descriptor = os.open('/tmp/fifo_cursor', os.O_RDONLY)
lectura = os.read(descriptor,3)
print('Lector 1 lee:', lectura)