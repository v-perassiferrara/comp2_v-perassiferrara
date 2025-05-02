
'''
Ejercicio 5: Simulación de cola de trabajos con señales
Objetivo: Simular un sistema productor-consumidor asíncrono usando señales.

Enunciado: Desarrolla dos procesos: uno productor y uno consumidor.
El productor genera trabajos (simulados por mensajes con timestamp) y,
al generarlos, envía SIGUSR1 al consumidor. El consumidor debe recibir la señal,
registrar el timestamp de recepción y "procesar" el trabajo (simulado con un sleep()).
Implementa una protección contra pérdida de señales: si se reciben varias en rápida sucesión,
deben encolarse en una estructura temporal para ser procesadas una por una.
'''

