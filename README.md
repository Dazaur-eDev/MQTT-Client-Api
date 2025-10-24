# Cliente MQTT con API REST

Una aplicación que combina un broker MQTT de código abierto (Mosquitto) con un cliente MQTT personalizado que expone una API REST para gestión de mensajes y suscripciones.
Pendiente de agregar la base de datos par darle persistencia a la data que se recibe.

## Arquitectura

El proyecto está compuesto por dos servicios principales:

- **Mosquitto Broker**: Servidor MQTT que maneja la comunicación entre clientes
- **Cliente MQTT**: Aplicación Python que se conecta al broker y expone una API REST

```
┌─────────────────┐    ┌─────────────────┐
│   Mosquitto     │    │   Cliente MQTT  │
│   (Broker)      │◄──►│   + API REST    │
│   Puerto: 1885  │    │   Puerto: 6000  │
└─────────────────┘    └─────────────────┘
```

## Requisitos y Puertos

- Python 3
- Flash 3.1.2
- paho_mqtt 2.1.0
- Docker Compose
- Puerto 1885 (Mosquitto)
- Puerto 6000 (API REST)
- Puerto 1883 y 9001 (Cliente MQTT) 
- [Mosquitto](https://mosquitto.org/download/)

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd Client_Mqtt_Icm
```

### 2. Configurar credenciales de Mosquitto

Generar archivo de contraseñas para Mosquitto:
```bash
docker run -it --rm -v ./mosquitto/config:/mosquitto/config eclipse-mosquitto:2.0 mosquitto_passwd -c /mosquitto/config/passwords 'tu_usuario'
```

**Nota**: Cuando se solicite, ingresar la contraseña, ingresas tu contraseña y esa misma debes registrar en el .env`)

### 3. Verificar configuración del entorno

Asegúrate de que el archivo `.env` contenga:
```env
MQTT_HOST=mosquitto
MQTT_PORT=1883
MQTT_USERNAME=tu_usuario
MQTT_PASSWORD=tu_contraseña
APP_LOG_LEVEL=INFO
```

## Ejecución

### Levantar toda la aplicación
```bash
docker-compose up -d
```

### Verificar que los servicios estén corriendo
```bash
docker-compose ps
```

Deberías ver algo como:
```
    Name                   Command               State                    Ports
mosquitto-server   /docker-entrypoint.sh /usr ...   Up      0.0.0.0:1885->1883/tcp
mqtt-app          python main.py                    Up      0.0.0.0:1883->1883/tcp, 0.0.0.0:6000->6000/tcp, 0.0.0.0:9001->9001/tcp
```

### Ver logs en tiempo real
```bash
# Logs de ambos servicios
docker-compose logs -f

# Solo Mosquitto
docker-compose logs -f mosquitto

# Solo cliente MQTT
docker-compose logs -f mqtt-app
```

## API REST

La aplicación expone una API REST en `http://localhost:6000` con los siguientes endpoints:

### Suscribirse a un topic
```bash
curl -X POST http://localhost:6000/subscribe \
  -H "Content-Type: application/json" \
  -d '{"topic": "sensors/temperature", "qos": 0}'
```

### Publicar un mensaje
```bash
curl -X POST http://localhost:6000/publish \
  -H "Content-Type: application/json" \
  -d '{"topic": "sensors/temperature", "message": "25.5", "qos": 0}'
```

### Listar topics suscritos
```bash
curl http://localhost:6000/topics
```

### Obtener mensajes recientes
```bash
curl http://localhost:6000/messages?limit=5
```

### Desuscribirse de un topic
```bash
curl -X POST http://localhost:6000/unsubscribe \
  -H "Content-Type: application/json" \
  -d '{"topic": "sensors/temperature"}'
```

### Cambiar suscripción de topic
```bash
curl -X POST http://localhost:6000/change_topic \
  -H "Content-Type: application/json" \
  -d '{"old_topic": "sensors/temperature", "new_topic": "sensors/humidity", "qos": 0}'
```

## Pruebas Rápidas

### Usando mosquitto_pub/sub (si tienes las herramientas instaladas)

**Terminal 1 - Suscriptor:**
```bash
mosquitto_sub -h localhost -p 1885 -u admin -P 227589Icm -t "test/topic"
```

**Terminal 2 - Publicador:**
```bash
mosquitto_pub -h localhost -p 1885 -u admin -P 227589Icm -t "test/topic" -m "Hola Mundo"
```

### Usando la API REST

**1. Suscribirse al topic:**
```bash
curl -X POST http://localhost:6000/subscribe \
  -H "Content-Type: application/json" \
  -d '{"topic": "test/topic", "qos": 0}'
```

**2. Publicar mensaje:**
```bash
curl -X POST http://localhost:6000/publish \
  -H "Content-Type: application/json" \
  -d '{"topic": "test/topic", "message": "Hola desde API", "qos": 0}'
```

**3. Ver mensajes recibidos:**
```bash
curl http://localhost:6000/messages
```

## Estructura del Proyecto

```
Client_Mqtt_Icm/
├── docker-compose.yml          # Configuración de servicios
├── Dockerfile                  # Imagen del cliente MQTT
├── requirements.txt            # Dependencias Python
├── .env                       # Variables de entorno
├── main.py                    # Punto de entrada principal
├── Core/                      # Lógica central MQTT
│   ├── client_mqtt.py         # Cliente MQTT principal
│   ├── connection_manager.py  # Gestión de conexiones
│   └── message_handler.py     # Procesamiento de mensajes
├── Config/                    # Configuraciones
│   └── settings.py           # Configuración MQTT
├── Services/                  # Servicios de aplicación
│   ├── api.py                # API REST Flask
│   └── message_processor.py  # Procesador de mensajes
├── Utils/                     # Utilidades
│   ├── logger.py             # Sistema de logging
│   └── validators.py         # Validadores
└── mosquitto/                # Configuración Mosquitto
    ├── config/
    │   ├── mosquitto.conf    # Configuración del broker
    │   └── passwords         # Archivo de contraseñas
    ├── data/                 # Datos persistentes
    └── log/                  # Logs del broker
```

## Configuración Avanzada

### Modificar configuración de Mosquitto

Edita `mosquitto/config/mosquitto.conf` para cambiar:
- Puertos de escucha
- Configuración de autenticación
- Niveles de logging
- Persistencia de datos

### Cambiar nivel de logging

Modifica `APP_LOG_LEVEL` en el archivo `.env`:
```env
APP_LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```



## Solución de Problemas

### El cliente no se conecta al broker
1. Verifica que Mosquitto esté corriendo: `docker-compose ps`
2. Revisa los logs: `docker-compose logs mosquitto`
3. Confirma las credenciales en `.env`

### Error de autenticación
1. Regenera el archivo de contraseñas
2. Reinicia los servicios: `docker-compose restart`

### Puerto ocupado
```bash
# Verificar qué está usando el puerto
lsof -i :6000
lsof -i :1885

# Cambiar puertos en docker-compose.yml si es necesario
```

### Ver logs detallados
```bash
# Logs con timestamp
docker-compose logs -f -t

# Logs de un servicio específico
docker-compose logs -f mqtt-app
```

## Seguridad

- Las contraseñas están en texto plano en `.env` (para desarrollo)
- En producción, usar secrets de Docker o variables de entorno seguras
- Mosquitto configurado con autenticación obligatoria
- Sin SSL/TLS configurado (añadir para producción)

## Monitoreo

- Logs de aplicación: `logs/app.log` dentro del contenedor
- Logs de Mosquitto: `mosquitto/log/mosquitto.log`

## Detener la Aplicación

```bash
# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# o mas agresivamente
docker compose down --volumes --remove-orphans

# Limpiar imágenes no utilizadas
docker system prune
```