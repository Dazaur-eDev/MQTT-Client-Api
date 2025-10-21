# main.py
import os
import threading
from Config.settings import MQTTConfig
from Core.client_mqtt import MQTTClient
from Services.message_processor import MessageProcessor
from Services.api import app, set_client_mqtt
from Utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    # Configuración del cliente MQTT central
    mqtt_config = MQTTConfig(
        host=os.getenv("MQTT_HOST", "localhost"),
        port=int(os.getenv("MQTT_PORT", 1883)),
        username=os.getenv("MQTT_USERNAME"),
        password=os.getenv("MQTT_PASSWORD"),
        client_id="mqtt_client_server"
    )

    client_mqtt = MQTTClient(mqtt_config)
    MessageProcessor(client_mqtt.message_handler)
    client_mqtt.start()
    logger.info("Servidor MQTT iniciado y corriendo...")

    # Asignar el cliente MQTT a la API
    set_client_mqtt(client_mqtt)

    # Iniciar API REST en hilo separado
    def run_api():
        app.run(host="0.0.0.0", port=5000)

    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    logger.info("API REST iniciada en hilo separado.")

    # Mantener vivo el contenedor sin consumir CPU
    stop_event = threading.Event()
    try:
        stop_event.wait()  # espera indefinida
    except KeyboardInterrupt:
        logger.info("Señal de shutdown recibida. Deteniendo servicios...")
        client_mqtt.stop()
        logger.info("Servidor MQTT detenido.")

if __name__ == "__main__":
    main()
