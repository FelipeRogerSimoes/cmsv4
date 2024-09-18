from flask import Blueprint, request, jsonify, send_file
from models import db, Timesheet, SystemUser, Case, Person
import logging
from datetime import datetime
from sqlalchemy.orm import aliased
from sqlalchemy import func
from openpyxl import Workbook
import os



def create_excel(data, filename, headers):
    wb = Workbook()
    ws = wb.active
    ws.title = "Timesheets Agrupados"

    # Adicionar cabeçalhos
    ws.append(headers)

    # Adicionar dados
    for entry in data:
        ws.append(list(entry.values()))

    # Salvar o arquivo
    filepath = os.path.join('downloads', filename)
    wb.save(filepath)
    return filepath




timesheet_bp = Blueprint('timesheet_bp', __name__)

# CREATE (POST) - Criar um novo timesheet
@timesheet_bp.route('/', methods=['POST'])
def create_timesheet():
    data = request.get_json()

    try:
        # Converter a string de data para objeto date do Python
        activity_date = datetime.strptime(data.get('activity_date'), '%Y-%m-%d').date()

        # Criar um novo objeto Timesheet
        new_timesheet = Timesheet(
            case_id=data.get('case_id'),
            billing_type=data.get('billing_type'),
            activity_type=data.get('activity_type'),
            lead_adjuster=data.get('lead_adjuster'),
            approved_by_manager=data.get('approved_by_manager'),
            approved_by_director=data.get('approved_by_director'),
            billed=data.get('billed'),
            invoice=data.get('invoice'),
            description=data.get('description'),
            activity_date=activity_date,  # Use o objeto de data convertido
            hours_worked=data.get('hours_worked'),
            rate=data.get('rate'),
            fee=data.get('fee'),
            excluded=data.get('excluded')
        )

        # Adicionar à sessão do banco de dados
        db.session.add(new_timesheet)
        db.session.commit()

        logging.info(f"Timesheet criado com sucesso.")
        return jsonify(new_timesheet.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar o timesheet: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todos os timesheets
@timesheet_bp.route('/', methods=['GET'])
def get_all_timesheets():
    # Realiza o join com as tabelas Case, SystemUser e Person para obter os nomes e os dados do caso
    timesheets = db.session.query(
        Timesheet,
        Case.case_number,
        Case.temporal,
        Person.name
    ).join(Case, Timesheet.case_id == Case.id) \
     .join(SystemUser, Timesheet.lead_adjuster == SystemUser.id) \
     .join(Person, SystemUser.person_id == Person.id) \
     .all()

    # Criar uma lista de dicionários contendo os timesheets e os dados adicionais
    timesheets_list = []
    for timesheet, case_number, temporal, lead_adjuster_name in timesheets:
        timesheet_dict = timesheet.to_dict()
        timesheet_dict['case_number'] = case_number  # Adiciona o case_number
        timesheet_dict['temporal'] = temporal  # Adiciona o temporal do caso
        timesheet_dict['lead_adjuster_name'] = lead_adjuster_name  # Adiciona o nome do regulador
        del timesheet_dict['lead_adjuster']  # Remove o ID do lead_adjuster
        del timesheet_dict['case_id']  # Remove o ID do case_id

        timesheets_list.append(timesheet_dict)

    return jsonify(timesheets_list), 200

# Função para obter timesheets agrupados com manager
def get_grouped_timesheets_with_manager_data():
    ManagerPerson = aliased(Person)

    # Consulta SQL para juntar Timesheet, SystemUser, Person e Manager
    results = db.session.query(
        Person.name.label('lead_adjuster_name'),
        Timesheet.activity_date,
        func.sum(Timesheet.hours_worked).label('total_hours'),
        func.sum(Timesheet.fee).label('total_fee'),
        ManagerPerson.name.label('manager_name')
    ).join(SystemUser, Timesheet.lead_adjuster == SystemUser.id) \
     .join(Person, SystemUser.person_id == Person.id) \
     .join(ManagerPerson, SystemUser.manager == ManagerPerson.id, isouter=True) \
     .filter(Timesheet.excluded == False) \
     .group_by(Person.name, Timesheet.activity_date, ManagerPerson.name) \
     .order_by(Timesheet.activity_date) \
     .all()

    # Transformar os resultados em uma lista de dicionários
    grouped_timesheets = []
    for result in results:
        grouped_timesheets.append({
            'lead_adjuster_name': result.lead_adjuster_name,
            'activity_date': result.activity_date.strftime('%Y-%m-%d'),
            'total_hours': float(result.total_hours),  # Converter para float
            'total_fee': float(result.total_fee),  # Converter para float
            'manager_name': result.manager_name  # Adiciona o nome do manager
        })

    return grouped_timesheets

# Endpoint para obter timesheets agrupados com manager
@timesheet_bp.route('/grouped_with_manager', methods=['GET'])
def get_grouped_timesheets_with_manager():
    grouped_data = get_grouped_timesheets_with_manager_data()
    return jsonify(grouped_data), 200

# Endpoint para gerar e baixar arquivo Excel de dados agrupados por dia
@timesheet_bp.route('/export_grouped_daily', methods=['GET'])
def export_grouped_timesheets_daily():
    results = get_grouped_timesheets_with_manager_data()

    # Criar o arquivo Excel
    filepath = create_excel(results, 'grouped_daily_timesheets.xlsx', ['Lead Adjuster', 'Activity Date', 'Total Hours', 'Total Fee', 'Manager'])

    # Enviar o arquivo para download
    return send_file(filepath, as_attachment=True)

# Endpoint para gerar e baixar arquivo Excel de dados agrupados por regulador e gestor
@timesheet_bp.route('/export_grouped_regulator_manager', methods=['GET'])
def export_grouped_timesheets_regulator_manager():
    results = get_grouped_timesheets_with_manager_data()

    # Criar o arquivo Excel
    filepath = create_excel(results, 'grouped_regulator_manager_timesheets.xlsx', ['Lead Adjuster', 'Activity Date', 'Total Hours', 'Total Fee', 'Manager'])

    # Enviar o arquivo para download
    return send_file(filepath, as_attachment=True)

# READ (GET) - Obter um timesheet específico pelo ID
@timesheet_bp.route('/<int:id>', methods=['GET'])
def get_timesheet(id):
    timesheet = Timesheet.query.get_or_404(id)
    return jsonify(timesheet.to_dict()), 200

# UPDATE (PUT) - Atualizar um timesheet pelo ID
@timesheet_bp.route('/<int:id>', methods=['PUT'])
def update_timesheet(id):
    timesheet = Timesheet.query.get_or_404(id)
    data = request.get_json()

    try:
        # Converter a string de data para objeto date do Python
        if 'activity_date' in data:
            timesheet.activity_date = datetime.strptime(data.get('activity_date'), '%Y-%m-%d').date()

        # Atualizar apenas os campos que foram enviados
        timesheet.case_id = data.get('case_id', timesheet.case_id)
        timesheet.billing_type = data.get('billing_type', timesheet.billing_type)
        timesheet.activity_type = data.get('activity_type', timesheet.activity_type)
        timesheet.lead_adjuster = data.get('lead_adjuster', timesheet.lead_adjuster)
        timesheet.approved_by_manager = data.get('approved_by_manager', timesheet.approved_by_manager)
        timesheet.approved_by_director = data.get('approved_by_director', timesheet.approved_by_director)
        timesheet.billed = data.get('billed', timesheet.billed)
        timesheet.invoice = data.get('invoice', timesheet.invoice)
        timesheet.description = data.get('description', timesheet.description)
        timesheet.hours_worked = data.get('hours_worked', timesheet.hours_worked)
        timesheet.rate = data.get('rate', timesheet.rate)
        timesheet.fee = data.get('fee', timesheet.fee)
        timesheet.excluded = data.get('excluded', timesheet.excluded)

        # Commit para salvar as mudanças no banco de dados
        db.session.commit()

        return jsonify(timesheet.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar o timesheet: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar um timesheet pelo ID
@timesheet_bp.route('/<int:id>', methods=['DELETE'])
def delete_timesheet(id):
    timesheet = Timesheet.query.get_or_404(id)

    try:
        db.session.delete(timesheet)
        db.session.commit()
        logging.info(f"Timesheet deletado com sucesso.")
        return jsonify({'message': 'Timesheet deletado com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar o timesheet: {e}")
        return jsonify({'error': str(e)}), 400
