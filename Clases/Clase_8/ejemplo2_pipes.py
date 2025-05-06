from multiprocessing import Pipe

parent_conn, child_conn = Pipe()
parent_conn.send("hola")
print(child_conn.recv())

child_conn.send("hola 2")
print(parent_conn.recv())