import paho.mqtt.client as mqtt
from Core.message_handler import MessageHandler
from Core.connection_manager import ConnectionManager
from Utils.logger import get_logger

class MQTTClient:
    def __init__(self, config):
        self.config = config
        self.client = mqtt.Client(client_id=config.client_id)
        self.message_handler = MessageHandler()
        self.connection_manager = ConnectionManager()
        self.logger = get_logger()
        self.current_topics = set()  # para trackear tópicos suscritos
        self._setup_callbacks()

    def _setup_callbacks(self):
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        self.logger.info(f"Conectado MQTT con código {rc}")

    def _on_disconnect(self, client, userdata, rc):
        self.logger.info("Desconectado MQTT")

    def _on_message(self, client, userdata, msg):
        self.message_handler.handle_message(msg)

    # Métodos para API REST
    def subscribe_topic(self, topic, qos=0):
        self.client.subscribe(topic, qos)
        self.current_topics.add(topic)
        self.logger.info(f"Suscrito al topic {topic} (QoS={qos})")

    def unsubscribe_topic(self, topic):
        self.client.unsubscribe(topic)
        self.current_topics.discard(topic)
        self.logger.info(f"Desuscrito del topic {topic}")

    def change_topic(self, old_topic, new_topic, qos=0):
        self.unsubscribe_topic(old_topic)
        self.subscribe_topic(new_topic, qos)
        self.logger.info(f"Cambio topic {old_topic} -> {new_topic} (QoS={qos})")

    def get_current_topics(self):
        return list(self.current_topics)


    # Métodos de inicio y stop
    def start(self):
        if self.config.username and self.config.password:
            self.client.username_pw_set(self.config.username, self.config.password)
        self.client.connect(self.config.host, self.config.port, self.config.keepalive)
        self.client.loop_start()  # usar loop_start para que corra en background

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
