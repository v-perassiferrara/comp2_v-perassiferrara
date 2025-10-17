import asyncio

class EstadoServidor:
    """Estado compartido entre todos los clientes"""
    def __init__(self):
        self.clientes_activos = 0
        self.mensajes_totales = 0

estado = EstadoServidor()

async def manejar_cliente(reader, writer):
    """Maneja un cliente individual"""
    addr = writer.get_extra_info('peername')
    print(f"🔌 Cliente conectado desde {addr}")
    
    estado.clientes_activos += 1
    
    try:
        # Mensaje de bienvenida
        writer.write(b"Bienvenido al servidor Echo!\n")
        writer.write(b"Comandos: /stats, /quit\n")
        await writer.drain()
        
        while True:
            # Leer datos (hasta 1024 bytes)
            data = await reader.read(1024)
            
            if not data:
                break
            
            mensaje = data.decode().strip()
            estado.mensajes_totales += 1
            
            # Procesar comandos
            if mensaje == "/quit":
                writer.write(b"Adios!\n")
                await writer.drain()
                break
                
            elif mensaje == "/stats":
                stats = (
                    f"Clientes activos: {estado.clientes_activos}\n"
                    f"Mensajes totales: {estado.mensajes_totales}\n"
                ).encode()
                writer.write(stats)
                await writer.drain()
                
            else:
                # Echo normal
                respuesta = f"Echo: {mensaje}\n".encode()
                writer.write(respuesta)
                await writer.drain()
    
    except Exception as e:
        print(f"❌ Error con cliente {addr}: {e}")
    
    finally:
        estado.clientes_activos -= 1
        print(f"👋 Cliente {addr} desconectado")
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        manejar_cliente,
        '127.0.0.1',
        8888
    )
    
    addr = server.sockets[0].getsockname()
    print(f"🚀 Servidor escuchando en {addr}")
    print("   Conéctate con: telnet localhost 8888")
    
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")