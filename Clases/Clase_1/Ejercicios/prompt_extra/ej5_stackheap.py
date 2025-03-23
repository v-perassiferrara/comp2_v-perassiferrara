# Crea una función que genere una lista grande (ej. [0]*1000) y verifica su dirección en memoria con id().
def create_list():
    blist = [0] * 10000
    print(len(blist))
    print(id(blist)) #direccion de memoria de la lista grande

create_list()

# print(len(blist))
# print(id(blist)) #direccion de memoria de la lista grande