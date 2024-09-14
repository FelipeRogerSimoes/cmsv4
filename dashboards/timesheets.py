from flask import Blueprint, render_template, send_from_directory
from openpyxl import Workbook
from config import Config
import os

timesheets_bp = Blueprint('timesheets_bp', __name__)


# Endpoint para exibir o dashboard de timesheets
@timesheets_bp.route('/')
def show_timesheets_dashboard():
    # Dados fictícios de timesheets (pode ser substituído pelos dados reais do banco de dados)
    timesheets_data = [
        {'id': 1, 'description': 'Análise de sistema', 'hours': 8},
        {'id': 2, 'description': 'Reunião com cliente', 'hours': 2},
        {'id': 3, 'description': 'Desenvolvimento de relatórios', 'hours': 5}
    ]

    # Renderizar o template HTML do dashboard
    return render_template('timesheets.html', timesheets=timesheets_data)


# Rota para gerar e baixar o arquivo Excel
@timesheets_bp.route('/download_excel', methods=['GET'])
def download_timesheet_excel():
    filename = "timesheet_report.xlsx"
    filepath = os.path.join(Config.DOWNLOAD_FOLDER, filename)

    # Gerar o arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Timesheet"

    # Adicionar cabeçalhos e dados
    ws.append(["ID", "Descrição", "Horas Trabalhadas"])
    timesheets_data = [
        {'id': 1, 'description': 'Análise de sistema', 'hours': 8},
        {'id': 2, 'description': 'Reunião com cliente', 'hours': 2},
        {'id': 3, 'description': 'Desenvolvimento de relatórios', 'hours': 5}
    ]
    for entry in timesheets_data:
        ws.append([entry['id'], entry['description'], entry['hours']])

    # Salvar o arquivo Excel no diretório de downloads
    wb.save(filepath)

    # Retornar o arquivo para download
    return send_from_directory(Config.DOWNLOAD_FOLDER, filename, as_attachment=True)
