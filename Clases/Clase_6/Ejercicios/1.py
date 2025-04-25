'''
Ejercicio 1 — Lectura diferida
Objetivo: Comprender el bloqueo de lectura en un FIFO.

Instrucciones:
    Crear un FIFO llamado /tmp/test_fifo.
    Ejecutar un script Python que intente leer desde el FIFO antes de que exista un escritor.
    En otro terminal, ejecutar un script que escriba un mensaje en el FIFO.

Preguntas:
    ¿Qué se observa en el lector mientras espera?
    Se queda "congelado" (bloqueado) hasta que el escritor envía un mensaje.
    
    ¿Qué ocurre si se escriben múltiples líneas desde el escritor?
    Se van recibiendo de a una en el lector.
    
'''