import argparse

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("El número de lineas debe ser entero y positivo")
    return ivalue



def main():
    parser = argparse.ArgumentParser(description="Ejercicio 2 de argparse")

    parser.add_argument("input", help="Archivo de entrada")
    parser.add_argument("-o", "--output", required=True, help="Archivo de salida")
    parser.add_argument("-l", "--lines", type=check_positive, default=5, help="Número de líneas a mostrar (entero positivo)")
    parser.add_argument("-m", "--mode", choices=["rapido", "lento"], help="Modo de procesamiento (rapido o lento)")
    parser.add_argument("--verbose", action="store_true", help="Muestra detalles del proceso")

    args = parser.parse_args()

    print(f"Procesando {args.lines} líneas del archivo {args.input} y guardando en {args.output} en procesamiento {args.mode}")

    if args.verbose == True:
        print("Modo detallado activado")

    



    

#Implementa un comando --help para que el usuario vea la documentación.







# with open(args.file, "r") as file:
#     lines = file.readlines()

# if args.reverse == True:
#     lines.reverse()

# for line in range (0, args.lines):
#     print(lines[line])

if __name__ == "__main__":
    main()