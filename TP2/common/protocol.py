"""
Protocolo de comunicación entre servidores
"""
import struct
import json


class ProtocolError(Exception):
    """Error en el protocolo de comunicación"""
    pass


class Protocol:
    """Protocolo de comunicación binario con longitud prefijada"""
    
    # Tamaño máximo de mensaje: 100 MB
    MAX_MESSAGE_SIZE = 100 * 1024 * 1024
    
    @staticmethod
    def encode_message(data):
        """
        Codifica un mensaje para envío
        
        Args:
            data: Diccionario con datos a enviar
        
        Returns:
            Bytes con longitud + mensaje JSON
            
        Raises:
            ProtocolError: Si el mensaje es demasiado grande
        """
        try:
            message_json = json.dumps(data).encode('utf-8')
            message_length = len(message_json)
            
            if message_length > Protocol.MAX_MESSAGE_SIZE:
                raise ProtocolError(
                    f"Mensaje demasiado grande: {message_length} bytes "
                    f"(máximo: {Protocol.MAX_MESSAGE_SIZE})"
                )
            
            length_prefix = struct.pack('!I', message_length)
            return length_prefix + message_json
        except (TypeError, ValueError) as e:
            raise ProtocolError(f"Error codificando mensaje: {e}")
    
    @staticmethod
    def decode_length(length_bytes):
        """
        Decodifica la longitud del mensaje
        
        Args:
            length_bytes: 4 bytes con la longitud
        
        Returns:
            Longitud del mensaje
            
        Raises:
            ProtocolError: Si los bytes son inválidos
        """
        if len(length_bytes) != 4:
            raise ProtocolError(
                f"Longitud inválida: se esperaban 4 bytes, "
                f"se recibieron {len(length_bytes)}"
            )
        
        try:
            length = struct.unpack('!I', length_bytes)[0]
            
            if length > Protocol.MAX_MESSAGE_SIZE:
                raise ProtocolError(
                    f"Longitud de mensaje excesiva: {length} bytes "
                    f"(máximo: {Protocol.MAX_MESSAGE_SIZE})"
                )
            
            return length
        except struct.error as e:
            raise ProtocolError(f"Error decodificando longitud: {e}")
    
    @staticmethod
    def decode_message(message_bytes):
        """
        Decodifica un mensaje JSON
        
        Args:
            message_bytes: Bytes del mensaje
        
        Returns:
            Diccionario con los datos
            
        Raises:
            ProtocolError: Si el mensaje es inválido
        """
        try:
            message_str = message_bytes.decode('utf-8')
            return json.loads(message_str)
        except UnicodeDecodeError as e:
            raise ProtocolError(f"Error decodificando UTF-8: {e}")
        except json.JSONDecodeError as e:
            raise ProtocolError(f"Error decodificando JSON: {e}")
    
    @staticmethod
    async def send_async(writer, data):
        """
        Envía un mensaje de forma asíncrona
        
        Args:
            writer: asyncio StreamWriter
            data: Diccionario con datos a enviar
            
        Raises:
            ProtocolError: Si hay error en la codificación
            ConnectionError: Si hay error en el envío
        """
        try:
            message = Protocol.encode_message(data)
            writer.write(message)
            await writer.drain()
        except (ConnectionError, BrokenPipeError) as e:
            raise ConnectionError(f"Error enviando mensaje: {e}")
    
    @staticmethod
    async def receive_async(reader):
        """
        Recibe un mensaje de forma asíncrona
        
        Args:
            reader: asyncio StreamReader
        
        Returns:
            Diccionario con los datos recibidos
            
        Raises:
            ProtocolError: Si el mensaje es inválido
            ConnectionError: Si la conexión se cierra
        """
        try:
            # Leer longitud del mensaje
            length_bytes = await reader.readexactly(4)
            if not length_bytes:
                raise ConnectionError("Conexión cerrada por el peer")
            
            message_length = Protocol.decode_length(length_bytes)
            
            # Leer mensaje completo
            message_bytes = await reader.readexactly(message_length)
            if not message_bytes:
                raise ConnectionError("Conexión cerrada antes de recibir el mensaje completo")
            
            return Protocol.decode_message(message_bytes)
            
        except ConnectionError:
            raise
        except Exception as e:
            if "connection" in str(e).lower():
                raise ConnectionError(f"Error de conexión: {e}")
            raise ProtocolError(f"Error recibiendo mensaje: {e}")
    
    @staticmethod
    def send_sync(sock, data):
        """
        Envía un mensaje de forma síncrona
        
        Args:
            sock: Socket TCP
            data: Diccionario con datos a enviar
            
        Raises:
            ProtocolError: Si hay error en la codificación
            ConnectionError: Si hay error en el envío
        """
        try:
            message = Protocol.encode_message(data)
            sock.sendall(message)
        except (ConnectionError, BrokenPipeError) as e:
            raise ConnectionError(f"Error enviando mensaje: {e}")
    
    @staticmethod
    def receive_sync(sock):
        """
        Recibe un mensaje de forma síncrona
        
        Args:
            sock: Socket TCP
        
        Returns:
            Diccionario con los datos recibidos
            
        Raises:
            ProtocolError: Si el mensaje es inválido
            ConnectionError: Si la conexión se cierra
        """
        try:
            # Leer longitud del mensaje
            length_bytes = sock.recv(4)
            if not length_bytes or len(length_bytes) < 4:
                raise ConnectionError("Conexión cerrada por el peer")
            
            message_length = Protocol.decode_length(length_bytes)
            
            # Leer mensaje completo en chunks
            message_bytes = b''
            while len(message_bytes) < message_length:
                chunk_size = min(4096, message_length - len(message_bytes))
                chunk = sock.recv(chunk_size)
                if not chunk:
                    raise ConnectionError("Conexión cerrada antes de recibir el mensaje completo")
                message_bytes += chunk
            
            return Protocol.decode_message(message_bytes)
            
        except ConnectionError:
            raise
        except Exception as e:
            if "connection" in str(e).lower():
                raise ConnectionError(f"Error de conexión: {e}")
            raise ProtocolError(f"Error recibiendo mensaje: {e}")
