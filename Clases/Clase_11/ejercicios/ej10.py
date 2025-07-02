## Ejercicio 10: Sincronización con `RLock`

Diseñe una clase `CuentaBancaria` con métodos `depositar` y `retirar`, ambos protegidos con un `RLock`. Permita que estos métodos se llamen recursivamente (desde otros métodos sincronizados).

Simule accesos concurrentes desde varios procesos.

---