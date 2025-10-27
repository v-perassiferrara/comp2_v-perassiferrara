'''
Ejercicio 3: Calculadora de números primos distribuida
Objetivo: Encontrar todos los números primos en un rango grande.

Requisitos:

Rango: 1 a 1,000,000
Dividir en chunks (ej: 100 chunks de 10,000 números)
Usar ProcessPoolExecutor para procesar chunks en paralelo
Implementar algoritmo eficiente (criba de Eratóstenes por chunk)
Comparar con versión secuencial
'''

from concurrent.futures import ProcessPoolExecutor
import time


def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def encontrar_primos_en_rango(inicio, fin):
    
    return [n for n in range(inicio, fin) if es_primo(n)]




if __name__ == "__main__":
    
    # Secuencial
    inicio_secuencial = time.time()
    primos_secuencial = encontrar_primos_en_rango(1, 1_000_000)
    fin_secuencial = time.time()
    print(f"Tiempo secuencial: {fin_secuencial - inicio_secuencial:.4f} segundos")
    
    print(f"Primos encontrados: {len(primos_secuencial)}")
    
    
    # Paralelo
    inicio_paralelo = time.time()
    primos_paralelo = []
    
    with ProcessPoolExecutor(max_workers=100) as executor:
        num_inicio = 1
        num_fin = 10_000
        
        futuros = []
        
        # Dividir el rango en chunks
        for i in range(100):
            futuro = executor.submit(encontrar_primos_en_rango, num_inicio, num_fin)
            futuros.append(futuro)
            num_inicio += 10_000
            num_fin += 10_000
            
        for i, futuro in enumerate(futuros):
            primos_paralelo.extend(futuro.result())
    
    fin_paralelo = time.time()
    print(f"Tiempo paralelo (100 chunks): {fin_paralelo - inicio_paralelo:.4f} segundos")
    
    print(f"Primos encontrados: {len(primos_paralelo)}")
    
    
    print(f"Mejora de tiempo: {(fin_secuencial - inicio_secuencial) / (fin_paralelo - inicio_paralelo):.2f}x")