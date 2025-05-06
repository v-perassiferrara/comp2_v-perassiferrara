from multiprocessing import Process

def saludo():
    print("Hola desde otro proceso")

if __name__ == '__main__':
    p = Process(target=saludo)
    p.start()
    p.join()