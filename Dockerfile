# Imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 y bcrypt
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto de Flask/Gunicorn
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Comando por defecto para desarrollo
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
