
from typing import Dict, List, Callable
from datetime import datetime

from Utils.logger import get_logger


class MessageHandler:
    def __init__(self):
        self.logger = get_logger()
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_filters: List[Callable] = []
        self.recent_messages: List[Dict] = []  # <- buffer de mensajes recientes

    def handle_message(self, msg):
        try:
            payload_str = msg.payload.decode('utf-8')
            message_data = {
                'topic': msg.topic,
                'payload': payload_str,
                'qos': msg.qos,
                'retain': msg.retain,
                'timestamp': datetime.now().isoformat()
            }

            self.logger.info(f"Mensaje recibido: {msg.topic} -> {payload_str}")

            # Guardar en buffer
            self.recent_messages.append(message_data)
            if len(self.recent_messages) > 100:  # límite configurable
                self.recent_messages.pop(0)

            if self._apply_filters(message_data):
                self._route_message(message_data)

        except Exception as e:
            self.logger.error(f"Error procesando mensaje: {e}")

    def _apply_filters(self, message_data: Dict) -> bool:
        """Aplica filtros a los mensajes"""
        for filter_func in self.message_filters:
            if not filter_func(message_data):
                return False
        return True

    def _route_message(self, message_data: Dict):
        """Enruta mensajes a suscriptores"""
        topic = message_data['topic']

        # Buscar suscriptores exactos
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(message_data)

        # Buscar suscriptores con wildcards
        self._handle_wildcard_routing(message_data)

    def _handle_wildcard_routing(self, message_data: Dict):
        """Maneja routing con wildcards + y #"""
        topic_parts = message_data['topic'].split('/')

        for subscribed_topic in self.subscribers:
            if self._topic_matches(topic_parts, subscribed_topic.split('/')):
                for callback in self.subscribers[subscribed_topic]:
                    callback(message_data)

    def _topic_matches(self, topic_parts: List[str], pattern_parts: List[str]) -> bool:
        """Verifica si un topic coincide con un patrón de wildcards"""
        if len(pattern_parts) == 0:
            return len(topic_parts) == 0

        if pattern_parts[0] == '#':
            return True

        if len(topic_parts) == 0:
            return False

        if pattern_parts[0] == '+' or pattern_parts[0] == topic_parts[0]:
            return self._topic_matches(topic_parts[1:], pattern_parts[1:])

        return False

    def add_subscriber(self, topic: str, callback: Callable):
        """Añade un suscriptor a un topic"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    def remove_subscriber(self, topic: str, callback: Callable):
        """Remueve un suscriptor de un topic"""
        if topic in self.subscribers:
            self.subscribers[topic].remove(callback)

    def add_filter(self, filter_func: Callable):
        """Añade un filtro de mensajes"""
        self.message_filters.append(filter_func)
