import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class MQTTConfig:
    host: str = "localhost"
    port: int = 1883
    keepalive: int = 60
    client_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    ca_cert: Optional[str] = None
    certfile: Optional[str] = None
    keyfile: Optional[str] = None


@dataclass
class BrokerConfig:
    log_level: str = "INFO"
    max_connections: int = 100
    message_size_limit: int = 1024
    retain_messages: bool = True