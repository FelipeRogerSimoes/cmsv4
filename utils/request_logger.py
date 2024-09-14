import os
from datetime import datetime
import pytz
from flask import request
from config import Config


# Função para registrar logs
def log_request(request_id):
    # Definir o fuso horário de Brasília
    timezone_brasilia = pytz.timezone('America/Sao_Paulo')

    # Obter data e hora atual no fuso horário de Brasília
    current_time = datetime.now(timezone_brasilia).strftime('%Y-%m-%d %H:%M:%S')

    # Criar a pasta de logs, se não existir
    if not os.path.exists(Config.LOG_FOLDER):
        os.makedirs(Config.LOG_FOLDER)

    # Nome do arquivo de log diário
    log_filename = os.path.join(Config.LOG_FOLDER, f"log_{datetime.now().strftime('%Y-%m-%d')}.txt")

    # Registrar os detalhes da requisição
    with open(log_filename, "a") as log_file:
        log_file.write(f"Request ID: {request_id}\n")
        log_file.write(f"Hora (Brasília): {current_time}\n")
        log_file.write(f"Headers: {request.headers}\n")
        log_file.write(f"Body: {request.get_data(as_text=True)}\n")
        log_file.write("=" * 50 + "\n")


# Função para mover o arquivo de log diário para a pasta de logs antigos
def move_old_log():
    log_filename = os.path.join(Config.LOG_FOLDER, f"log_{datetime.now().strftime('%Y-%m-%d')}.txt")
    if os.path.exists(log_filename):
        # Criar a pasta de logs antigos, se não existir
        if not os.path.exists(Config.OLD_LOG_FOLDER):
            os.makedirs(Config.OLD_LOG_FOLDER)

        # Mover o arquivo para a pasta de logs antigos
        old_log_filename = os.path.join(Config.OLD_LOG_FOLDER, os.path.basename(log_filename))
        os.rename(log_filename, old_log_filename)
        print(f"Log movido para {old_log_filename}")
