# HACER ESTO


def trabajador():
    """Un trabajador que recibe instrucciones y las ejecuta"""
    print("Trabajador listo. Esperando instrucciones...")
    
    while True:
        instruccion = yield
        
        if instruccion == "sumar":
            resultado = yield "Dame dos números"
            a, b = resultado
            print(f"Suma: {a} + {b} = {a + b}")
            
        elif instruccion == "terminar":
            print("Finalizando trabajo...")
            break
            
        else:
            print(f"Instrucción desconocida: {instruccion}")

# Usar el trabajador
w = trabajador()
next(w)  # Iniciar

w.send("sumar")
respuesta = w.send((10, 5))
print(f"El trabajador respondió: {respuesta}")

w.send("sumar")
w.send((100, 50))

w.send("terminar")