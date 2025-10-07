def eco_mejorado():
    print("Generador iniciado, esperando mensajes...")
    while True:
        mensaje = yield # Esto permite recibir un valor mientras está pausado
        print(f"Recibí: {mensaje}")


dialogo = eco_mejorado()    # creamos el generador

next(dialogo)  # "Arrancar" el generador hasta el primer yield

# Send permite inyectar un dato al yield ("incluye un next", no hay que hacerlo explícitamente)

dialogo.send("Hola")       # Recibí: Hola
dialogo.send("¿Qué tal?")  # Recibí: ¿Qué tal?