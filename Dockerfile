# Usa la imagen base de Python
FROM python:3.12

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Copia todo el contenido del directorio actual al contenedor en /app
COPY . .

# Exponer el puerto 8000 para que pueda ser accedido externamente
EXPOSE 8080

# Comando para ejecutar la aplicación Django en el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
