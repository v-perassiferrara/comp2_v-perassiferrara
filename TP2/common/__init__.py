"""
Módulo común con utilidades compartidas
"""
from .protocol import Protocol
from .serialization import serialize, deserialize

__all__ = ['Protocol', 'serialize', 'deserialize']
