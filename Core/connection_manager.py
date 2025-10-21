# core/connection_manager.py
import logging
from typing import Dict, Set
from datetime import datetime
from Utils.logger import get_logger


class ConnectionManager:
    def __init__(self):
        self.logger = get_logger()
        self.active_connections: Dict[str, Dict] = {}
        self.connection_stats = {
            'total_connections': 0,
            'active_connections': 0,
            'failed_connections': 0
        }

    def on_connect(self, client, rc):
        """Maneja conexiones exitosas"""
        if rc == 0:
            client_id = getattr(client, '_client_id', 'unknown')
            self.active_connections[client_id] = {
                'connected_at': datetime.now(),
                'client': client,
                'status': 'connected'
            }
            self.connection_stats['total_connections'] += 1
            self.connection_stats['active_connections'] += 1
            self.logger.info(f"Cliente conectado: {client_id}")
        else:
            self.connection_stats['failed_connections'] += 1
            self.logger.error(f"Conexión fallida con código: {rc}")

    def on_disconnect(self, client, rc):
        """Maneja desconexiones"""
        client_id = getattr(client, '_client_id', 'unknown')
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            self.connection_stats['active_connections'] -= 1
            self.logger.info(f"Cliente desconectado: {client_id}")

    def get_connection_stats(self) -> Dict:
        """Retorna estadísticas de conexiones"""
        return {
            **self.connection_stats,
            'current_active': len(self.active_connections)
        }

    def get_active_clients(self) -> Set[str]:
        """Retorna lista de clientes activos"""
        return set(self.active_connections.keys())
