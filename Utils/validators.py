
class MessageValidator:
    @staticmethod
    def validate_topic(topic: str) -> bool:
        """Valida formato de topic MQTT"""
        if not topic or len(topic) > 65535:
            return False
        # No debe contener caracteres null
        if '\x00' in topic:
            return False
        return True

    @staticmethod
    def validate_payload_size(payload: bytes, max_size: int = 1024) -> bool:
        """Valida tamaño del payload"""
        return len(payload) <= max_size

    @staticmethod
    def validate_qos(qos: int) -> bool:
        """Valida nivel QoS"""
        return qos in [0, 1, 2]