from flask import Flask, send_from_directory, abort, jsonify, request
from file_management import list_files
from config import Config
from controllers.person_controller import person_bp
from controllers.cases_controller import cases_bp
from dashboards.timesheets import timesheets_bp
from dashboards.casos import casos_bp
from threading import Thread
import time
import schedule
from utils.request_logger import log_request, move_old_log  # Serviço de logging
from email_service import process_email_attachments, check_invoices_email  # Serviço de e-mails

app = Flask(__name__)
app.config.from_object(Config)

# Registrar os blueprints para os dashboards e os CRUDs
app.register_blueprint(person_bp, url_prefix='/api/person')
app.register_blueprint(cases_bp, url_prefix='/api/cases')
app.register_blueprint(timesheets_bp, url_prefix='/dashboard/timesheets')
app.register_blueprint(casos_bp, url_prefix='/dashboard/casos')

# Middleware para interceptar requisições e registrar logs
@app.before_request
def before_request_logging():
    request_id = request.headers.get('X-Request-ID', 'unknown')  # Adicionar um ID à requisição, se disponível
    log_request(request_id)

# Listar todos os arquivos disponíveis na pasta de downloads
@app.route('/download')
def list_downloads():
    files = list_files(Config.DOWNLOAD_FOLDER)
    return jsonify({'files': files})

# Endpoint para baixar um arquivo específico de qualquer formato (PDF, Word, Excel, PPT)
@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(Config.DOWNLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

# Endpoint para baixar arquivos movidos para o backup
@app.route('/backup/<filename>')
def download_backup_file(filename):
    try:
        return send_from_directory(Config.BACKUP_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

# Função para agendar o serviço de leitura de e-mails
def schedule_email_reader():
    while True:
        try:
            # Agendar o serviço de processamento de anexos a cada 1 minuto para testar
            schedule.every(1).minutes.do(process_email_attachments)

            # Agendar o novo serviço de verificação de faturas a cada 1 minuto para testar
            schedule.every(1).minutes.do(check_invoices_email)

            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(f"Erro no serviço de e-mails: {e}")

# Função que inicializa a thread para rodar o serviço de e-mails em paralelo
def start_email_service():
    email_thread = Thread(target=schedule_email_reader)
    email_thread.daemon = True  # Isso garante que a thread seja fechada quando a aplicação Flask for encerrada
    email_thread.start()

# Função para agendar o serviço de movimentação dos logs diários
def schedule_log_movement():
    while True:
        try:
            schedule.every().day.at("23:59").do(move_old_log)  # Mover logs no final do dia
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(f"Erro no serviço de movimentação de logs: {e}")

# Função que inicializa a thread para rodar o serviço de logs em paralelo
def start_log_service():
    log_thread = Thread(target=schedule_log_movement)
    log_thread.daemon = True  # Isso garante que a thread seja fechada quando a aplicação Flask for encerrada
    log_thread.start()

if __name__ == '__main__':
    # Iniciar o serviço de e-mails e de logs em threads separadas
    start_email_service()
    start_log_service()

    # Rodar o servidor Flask
    app.run(debug=True)
