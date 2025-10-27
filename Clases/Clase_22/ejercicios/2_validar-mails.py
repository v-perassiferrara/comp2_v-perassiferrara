
'''
Ejercicio 2: Validador de emails concurrente
Objetivo: Validar emails verificando si el dominio existe (DNS lookup).

Requisitos:

Tener una lista de 100 emails
Para cada email, hacer DNS lookup del dominio (I/O-bound)
Usar ThreadPoolExecutor con 20 workers
Clasificar: válidos, inválidos, no verificables
Implementar timeout de 5s por verificación
'''


import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

def verificar_email(email):
    try:
        dominio = email.split('@')[1]
        # DNS lookup (I/O-bound)
        dns.resolver.resolve(dominio, 'MX')
        return ('valido')
    except Exception:
        return ('invalido')

def main():
    emails = [f'user{i}@gmail.com' for i in range(40)] + \
             [f'user{i}@yahoo.com' for i in range(30)] + \
             [f'user{i}@hotmail.com' for i in range(20)] + \
             [f'user{i}@dominio-inexistente-12345.com' for i in range(10)]

    validos = []
    invalidos = []
    no_verificables = []    # no verificables = dan timeout al hacer la verificación

    with ThreadPoolExecutor(max_workers=20) as executor:
        
        # envio al executor la tarea de verificación para cada email
        future_to_email = {executor.submit(verificar_email, email): email for email in emails}
        
        # a medida que terminan, se procesan
        for future in as_completed(future_to_email):
            email = future_to_email[future]
            try:
                status = future.result(timeout=5)
                if status == 'valido':
                    validos.append(email)
                else:
                    invalidos.append(email)
                    
            except TimeoutError:
                no_verificables.append(email)
                
            except Exception:
                invalidos.append(email)

    print(f"Emails válidos: {len(validos)}")
    print(f"Emails inválidos: {len(invalidos)}")
    print(f"Emails no verificables (timeout): {len(no_verificables)}")

if __name__ == "__main__":
    main()
