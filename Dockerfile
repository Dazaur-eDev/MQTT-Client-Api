# Imagen base liviana con Python
FROM python:3.10-slim

# Variables de entorno recomendadas
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al contenedor
COPY . .

# Crear carpetas necesarias con permisos seguros
RUN mkdir -p logs config \
    && chmod -R 755 logs config \
    && chown -R root:root logs config

# Exponer los puertos MQTT, WebSocket y API REST
EXPOSE 1883 9001 5000

# Comando por defecto al iniciar el contenedor
CMD ["python", "main.py"]
