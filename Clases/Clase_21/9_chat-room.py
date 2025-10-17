import asyncio

"""
Ejercicio 9: Chat room simple

Objetivo: Implementar un servidor de chat donde múltiples clientes pueden enviarse mensajes.

Requisitos:

    Servidor TCP que acepta múltiples clientes
    Cuando un cliente se conecta, pide su nombre
    Los mensajes de un cliente se broadcast a todos los demás
    Comandos: /list (mostrar usuarios), /quit (desconectar)
    Notificar a todos cuando alguien entra o sale

Pistas:

    Mantén un diccionario de {writer: nombre} para clientes activos
    Necesitas una función para broadcast a todos los clientes
    Usa try/except para manejar desconexiones abruptas
"""


clientes = {}  # {writer: addr} porque no tienen un "nombre"


async def broadcast(mensaje, remitente=None):
    # Enviar mensaje a todos excepto remitente
    for writer in clientes.keys():
        if writer != remitente:
            writer.write(mensaje.encode())
            await writer.drain()


async def manejar_cliente(reader, writer):
    """Maneja un cliente individual"""
    addr = writer.get_extra_info("peername")
    print(f"🔌 Cliente conectado desde {addr}")

    clientes[writer] = addr

    # Broadcast a todos los clientes
    await broadcast(f"Entró a la sala: {addr}", writer)

    try:
        # Mensaje de bienvenida
        writer.write(b"Bienvenido al servidor de chat!\n")
        writer.write(b"Comandos: /list, /quit\n")
        await writer.drain()

        while True:
            # Leer datos (hasta 1024 bytes)
            data = await reader.read(1024)

            if not data:
                break

            try:
                mensaje = data.decode().strip()

            except UnicodeDecodeError:
                print(f"⚠️  Cliente {addr} se desconectó de forma abrupta.")
                break

            # Procesar comandos (lista de usuarios, salir o mandar mensaje)
            if mensaje == "/quit":
                writer.write(b"Adios!\n")
                await writer.drain()
                break

            elif mensaje == "/list":
                lista_usuarios = "Usuarios conectados:\n" + "\n".join(
                    f"- {n}" for n in clientes.values()
                )
                writer.write(f"{lista_usuarios}\n".encode())
                await writer.drain()

            else:
                await broadcast(f"{addr}: {mensaje}", writer)

    except Exception as e:
        print(f"❌ Error con cliente {addr}: {e}")

    finally:
        clientes.pop(writer)
        await broadcast(f"Salió de la sala: {addr}", writer)
        print(f"👋 Cliente {addr} desconectado")
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(manejar_cliente, "127.0.0.1", 8888)

    addr = server.sockets[0].getsockname()
    print(f"🚀 Servidor escuchando en {addr}")
    print("   Conéctate con: telnet localhost 8888")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer detenido")
