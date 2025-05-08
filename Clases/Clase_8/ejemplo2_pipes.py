from multiprocessing import Pipe

# Crea un Pipe. Devuelve dos objetos de conexion, uno para cada extremo del pipe.
parent_conn, child_conn = Pipe()

# Envia un mensaje desde la conexion padre a la conexion hijo
parent_conn.send("hola")
# Recibe el mensaje en la conexion hijo e imprime
print(child_conn.recv())

# Envia un mensaje desde la conexion hijo a la conexion padre
child_conn.send("hola 2")
# Recibe el mensaje en la conexion padre e imprime
print(parent_conn.recv())

