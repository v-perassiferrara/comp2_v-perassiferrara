"""
Serialización de datos
"""
import json
import pickle


def serialize(data, format='json'):
    """
    Serializa datos
    
    Args:
        data: Datos a serializar
        format: 'json' o 'pickle'
    
    Returns:
        Bytes serializados
    """
    if format == 'json':
        return json.dumps(data).encode('utf-8')
    elif format == 'pickle':
        return pickle.dumps(data)
    else:
        raise ValueError(f"Formato desconocido: {format}")


def deserialize(data, format='json'):
    """
    Deserializa datos
    
    Args:
        data: Bytes serializados
        format: 'json' o 'pickle'
    
    Returns:
        Datos deserializados
    """
    if format == 'json':
        return json.loads(data.decode('utf-8'))
    elif format == 'pickle':
        return pickle.loads(data)
    else:
        raise ValueError(f"Formato desconocido: {format}")
