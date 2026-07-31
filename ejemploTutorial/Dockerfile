# Imagen base: interprete de Python sobre una Debian reducida
FROM python:3.12-slim

# Variables del interprete: no generar ficheros .pyc y no almacenar
# la salida en un buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

# Directorio de trabajo dentro de la imagen
WORKDIR /app

# Primero las dependencias: si no cambian, Docker reutiliza la capa
# de la instalacion aunque el codigo si haya cambiado
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ahora el codigo del proyecto
COPY . .

# Se recopilan los ficheros estaticos en STATIC_ROOT
RUN python manage.py collectstatic --noinput

# Directorio de datos (base de datos SQLite)
ENV DJANGO_DATA_DIR=/data
RUN mkdir -p /data

# Puerto en el que escuchara el servidor dentro del contenedor
EXPOSE 8000

# Orden de arranque: aplicar migraciones y lanzar Gunicorn
CMD ["sh", "-c", "python manage.py makemigrations encuestas && python manage.py migrate --noinput && gunicorn ejemploTutorial.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
