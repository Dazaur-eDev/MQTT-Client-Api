from flask import Flask, request, jsonify
from Utils.validators import MessageValidator
from Utils.logger import get_logger

app = Flask(__name__)
logger = get_logger()

# Variable global para el cliente central
client_mqtt_instance = None

def set_client_mqtt(client):
    """Asigna el cliente MQTT central a la API"""
    global client_mqtt_instance
    client_mqtt_instance = client
    logger.info("Cliente MQTT central asignado a la API.")

# ----------------------------
# Endpoint: Suscribirse a un topic
# ----------------------------
@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    topic = data.get("topic")
    qos = data.get("qos", 0)

    if not MessageValidator.validate_topic(topic):
        return jsonify({"status": "error", "message": "Tópico inválido"}), 400

    client_mqtt_instance.subscribe_topic(topic, qos)
    return jsonify({"status": "ok", "subscribed": topic, "qos": qos})

# ----------------------------
# Endpoint: Desuscribirse de un topic
# ----------------------------
@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    data = request.json
    topic = data.get("topic")

    if topic not in client_mqtt_instance.get_current_topics():
        return jsonify({"status": "error", "message": "No estaba suscrito"}), 400

    client_mqtt_instance.unsubscribe_topic(topic)
    return jsonify({"status": "ok", "unsubscribed": topic})

# ----------------------------
# Endpoint: Cambiar topic
# ----------------------------
@app.route("/change_topic", methods=["POST"])
def change_topic():
    data = request.json
    old_topic = data.get("old_topic")
    new_topic = data.get("new_topic")
    qos = data.get("qos", 0)

    if not MessageValidator.validate_topic(new_topic):
        return jsonify({"status": "error", "message": "Nuevo tópico inválido"}), 400

    client_mqtt_instance.change_topic(old_topic, new_topic, qos)
    return jsonify({"status": "ok", "old_topic": old_topic, "new_topic": new_topic, "qos": qos})

# ----------------------------
# Endpoint: Listar tópicos suscritos actualmente
# ----------------------------
@app.route("/topics", methods=["GET"])
def list_topics():
    return jsonify({"subscribed_topics": client_mqtt_instance.get_current_topics()})

# ----------------------------
# Endpoint: Publicar mensaje en un topic
# ----------------------------
@app.route("/publish", methods=["POST"])
def publish():
    data = request.json
    topic = data.get("topic")
    message = data.get("message")
    qos = data.get("qos", 0)

    if not MessageValidator.validate_topic(topic):
        return jsonify({"status": "error", "message": "Tópico inválido"}), 400

    client_mqtt_instance.client.publish(topic, payload=message, qos=qos)
    logger.info(f"Publicado mensaje en {topic}: {message}")
    return jsonify({"status": "ok", "topic": topic, "message": message, "qos": qos})

@app.route("/messages", methods=["GET"])
def get_messages():
    limit = int(request.args.get("limit", 10))
    messages = client_mqtt_instance.message_handler.recent_messages[-limit:]
    return jsonify({"count": len(messages), "messages": messages})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
