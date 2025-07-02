## Ejercicio 11: Manejo de Señales

Cree un script que instale un manejador para la señal `SIGUSR1`. El proceso deberá estar en espera pasiva (`pause()` o bucle infinito).

Desde Bash, envíe la señal al proceso con `kill -SIGUSR1 [pid]` y verifique la respuesta.

---