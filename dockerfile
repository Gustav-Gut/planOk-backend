# 1. Imagen base
FROM python:3.10-slim

# 2. Directorio de trabajo
WORKDIR /app

# 3. Copiar el archivo de dependencias
COPY requirements.txt /app/

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código
COPY . /app/

# 6. Exponer el puerto y definir el comando por defecto
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
