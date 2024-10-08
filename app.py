from flask import Flask, send_from_directory, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Importar o Migrate
from file_management import list_files
from config import Config
from controllers.person_controller import person_bp
from controllers.cases_controller import cases_bp
from controllers.routine_controller import routine_bp
from dashboards.timesheets import timesheets_bp
from dashboards.casos import casos_bp
from controllers.task_controller import task_bp
from controllers.expense_controller import expense_bp
from controllers.document_controller import document_bp
from controllers.event_controller import event_bp
from controllers.action_controller import action_bp
from controllers.parameter_controller import parameter_bp
from controllers.validation_controller import validation_bp
from controllers.field_controller import field_bp
from controllers.insurance_company_controller import insurance_company_bp
from controllers.system_user_controller import system_user_bp
from controllers.operations_controller import operations_bp
from controllers.rate_controller import rate_bp
from controllers.timesheet_controller import timesheet_bp
from controllers.goals_controller import goals_bp


from threading import Thread
import time
import schedule
from utils.request_logger import log_request, move_old_log  # Serviço de logging
from email_service import process_email_attachments, check_invoices_email  # Serviço de e-mails
from models import db  # Certifique-se de importar sua instância de SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Inicializar a instância do SQLAlchemy
db.init_app(app)  # Inicialize o SQLAlchemy com o app

# Criar tabelas automaticamente ao iniciar o servidor, caso ainda não existam
with app.app_context():
    db.create_all()

# Registrar os blueprints para os dashboards e os CRUDs
app.register_blueprint(person_bp, url_prefix='/api/person')
app.register_blueprint(cases_bp, url_prefix='/api/cases')
app.register_blueprint(timesheets_bp, url_prefix='/dashboard/timesheets')
app.register_blueprint(casos_bp, url_prefix='/dashboard/casos')
app.register_blueprint(routine_bp, url_prefix='/api/routine')
app.register_blueprint(task_bp, url_prefix='/api/task')
app.register_blueprint(expense_bp, url_prefix='/api/expense')
app.register_blueprint(document_bp, url_prefix='/api/document')
app.register_blueprint(event_bp, url_prefix='/api/event')
app.register_blueprint(action_bp, url_prefix='/api/action')
app.register_blueprint(parameter_bp, url_prefix='/api/parameter')
app.register_blueprint(validation_bp, url_prefix='/api/validation')
app.register_blueprint(field_bp, url_prefix='/api/field')
app.register_blueprint(insurance_company_bp, url_prefix='/api/insurance_company')
app.register_blueprint(system_user_bp, url_prefix='/api/system_user')
app.register_blueprint(operations_bp, url_prefix='/api/operations')
app.register_blueprint(rate_bp, url_prefix='/api/rate')
app.register_blueprint(timesheet_bp, url_prefix='/api/timesheet')
app.register_blueprint(goals_bp, url_prefix='/api/goals')



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
    # O contexto da aplicação é usado uma vez, antes de iniciar os agendamentos
    with app.app_context():
        schedule.every(1).minutes.do(process_email_attachments)  # Agendar o serviço de anexos a cada 1 minuto
        schedule.every(1).minutes.do(check_invoices_email)  # Agendar o serviço de faturas a cada 1 minuto
        while True:
            try:
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
    # O contexto da aplicação é usado uma vez, antes de iniciar os agendamentos
    with app.app_context():
        schedule.every().day.at("23:59").do(move_old_log)  # Mover logs no final do dia
        while True:
            try:
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
