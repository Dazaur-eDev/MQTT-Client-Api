# services/message_processor.py
import json
from typing import Dict, Any

from Core.message_handler import MessageHandler
from Utils.logger import get_logger


class MessageProcessor:
    def __init__(self, message_handler: MessageHandler):
        self.message_handler = message_handler
        self.logger = get_logger()
        self._setup_default_handlers()

    def _setup_default_handlers(self):
        """Configura manejadores por defecto"""
        self.message_handler.add_subscriber('system/status', self._handle_system_status)
        self.message_handler.add_subscriber('sensors/+', self._handle_sensor_data)
        self.message_handler.add_subscriber('commands/#', self._handle_commands)

    def _handle_system_status(self, message_data: Dict):
        """Maneja mensajes de estado del sistema"""
        self.logger.info(f"Estado del sistema: {message_data['payload']}")

    def _handle_sensor_data(self, message_data: Dict):
        """Procesa datos de sensores"""
        try:
            sensor_data = json.loads(message_data['payload'])
            sensor_id = message_data['topic'].split('/')[-1]
            self.logger.info(f"Datos de sensor {sensor_id}: {sensor_data}")
            # Aquí puedes añadir lógica de procesamiento específica
        except json.JSONDecodeError:
            self.logger.error("Error decodificando datos de sensor")

    def _handle_commands(self, message_data: Dict):
        """Procesa comandos"""
        command_topic = message_data['topic']
        command_payload = message_data['payload']
        self.logger.info(f"Comando recibido en {command_topic}: {command_payload}")

