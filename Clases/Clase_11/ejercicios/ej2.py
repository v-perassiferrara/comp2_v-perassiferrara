## Ejercicio 2: Proceso Zombi
'''
Cree un script que genere un proceso hijo que finaliza inmediatamente.

El padre no deberá recolectar su estado
hasta al menos 10 segundos después. 

Desde Bash, usar `ps` y `/proc/[pid]/status`
para identificar el estado Z (zombi) del hijo.
'''

import os
