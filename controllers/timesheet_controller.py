from flask import Blueprint, request, jsonify
from models import db, Timesheet
import logging
from datetime import datetime

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
    timesheets = Timesheet.query.all()
    return jsonify([timesheet.to_dict() for timesheet in timesheets]), 200

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
