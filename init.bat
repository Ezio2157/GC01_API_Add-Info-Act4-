@echo off
REM Instalar dependencias
pip3 install -r requirements.txt
REM Ejecutar el servidor Swagger
python -m swagger_server
