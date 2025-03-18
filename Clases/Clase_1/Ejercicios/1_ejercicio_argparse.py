import argparse

parser = argparse.ArgumentParser(description="Ejercicio 1 de argparse")

parser.add_argument("-f", "--file", required=True, help="Archivo de entrada")
parser.add_argument("-l", "--lines", type=int, default=5, required=False, help="Número de líneas a mostrar")
parser.add_argument("-r", "--reverse", action="store_true", help="Mostrar en orden inverso")

args = parser.parse_args()

with open(args.file, "r") as file:
    lines = file.readlines()

if args.reverse == True:
    lines.reverse()

for line in range (0, args.lines):
    print(lines[line])