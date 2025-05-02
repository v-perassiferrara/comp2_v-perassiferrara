
'''
Ejercicio 4: Control multihilo con señales externas
Objetivo: Integrar señales con hilos y control de ejecución.

Enunciado: Crea un programa multihilo donde un hilo cuenta regresivamente desde 30.
Usa una variable global con threading.Lock() para permitir que otro proceso externo,
al enviar una señal (SIGUSR1), pause la cuenta y otra señal (SIGUSR2) la reinicie.
El hilo principal debe instalar los handlers y proteger correctamente el estado compartido.
'''

