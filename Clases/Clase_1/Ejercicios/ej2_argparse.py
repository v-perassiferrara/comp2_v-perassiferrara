import argparse

parser = argparse.ArgumentParser(description="Ejemplo de argparse")
parser.add_argument("-i", "--input", required=True, help="Archivo de entrada")
parser.add_argument("-o", "--output", required=True, help="Archivo de salida")
args = parser.parse_args()

print(f"Archivo de entrada: {args.input}")
print(f"Archivo de salida: {args.output}")