"""
Protocolo de comunicación entre servidores
"""
import struct
import json


class Protocol:
    """Protocolo de comunicación binario con longitud prefijada"""
    
    @staticmethod
    def encode_message(data):
        """
        Codifica un mensaje para envío
        
        Args:
            data: Diccionario con datos a enviar
        
        Returns:
            Bytes con longitud + mensaje JSON
        """
        message_json = json.dumps(data).encode('utf-8')
        message_length = struct.pack('!I', len(message_json))
        return message_length + message_json
    
    @staticmethod
    def decode_length(length_bytes):
        """
        Decodifica la longitud del mensaje
        
        Args:
            length_bytes: 4 bytes con la longitud
        
        Returns:
            Longitud del mensaje
        """
        return struct.unpack('!I', length_bytes)[0]
    
    @staticmethod
    def decode_message(message_bytes):
        """
        Decodifica un mensaje JSON
        
        Args:
            message_bytes: Bytes del mensaje
        
        Returns:
            Diccionario con los datos
        """
        return json.loads(message_bytes.decode('utf-8'))
    
    @staticmethod
    async def send_async(writer, data):
        """
        Envía un mensaje de forma asíncrona
        
        Args:
            writer: asyncio StreamWriter
            data: Diccionario con datos a enviar
        """
        message = Protocol.encode_message(data)
        writer.write(message)
        await writer.drain()
    
    @staticmethod
    async def receive_async(reader):
        """
        Recibe un mensaje de forma asíncrona
        
        Args:
            reader: asyncio StreamReader
        
        Returns:
            Diccionario con los datos recibidos
        """
        length_bytes = await reader.readexactly(4)
        message_length = Protocol.decode_length(length_bytes)
        message_bytes = await reader.readexactly(message_length)
        return Protocol.decode_message(message_bytes)
