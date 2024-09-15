from flask import Blueprint, request, jsonify
from models import db, Routine
import logging
from datetime import datetime  # Import para manipulação de datas

routine_bp = Blueprint('routine_bp', __name__)

# CREATE (POST) - Criar uma nova rotina
@routine_bp.route('/', methods=['POST'])
def create_routine():
    data = request.get_json()

    try:
        # Converter a string 'start_date' para um objeto datetime
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()

        # Criar um novo objeto Routine
        new_routine = Routine(
            case_id=data.get('case_id'),
            name=data.get('name'),
            status=data.get('status'),
            start_date=start_date  # Usar o objeto datetime para 'start_date'
        )

        # Adicionar à sessão do banco de dados
        db.session.add(new_routine)
        db.session.commit()

        logging.info(f"Rotina {new_routine.name} criada com sucesso.")
        return jsonify(new_routine.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar a rotina: {e}")
        return jsonify({'error': str(e)}), 400


# READ (GET) - Obter todas as rotinas
@routine_bp.route('/', methods=['GET'])
def get_all_routines():
    routines = Routine.query.all()
    return jsonify([routine.to_dict() for routine in routines]), 200


# READ (GET) - Obter uma rotina específica pelo ID
@routine_bp.route('/<int:id>', methods=['GET'])
def get_routine(id):
    routine = Routine.query.get_or_404(id)
    return jsonify(routine.to_dict()), 200


# UPDATE (PUT) - Atualizar uma rotina pelo ID
@routine_bp.route('/<int:id>', methods=['PUT'])
def update_routine(id):
    routine = Routine.query.get_or_404(id)
    data = request.get_json()

    try:
        # Atualizar apenas os campos que foram enviados
        routine.case_id = data.get('case_id', routine.case_id)
        routine.name = data.get('name', routine.name)
        routine.status = data.get('status', routine.status)

        # Verificar se 'start_date' foi fornecido e convertê-lo
        if 'start_date' in data:
            routine.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()

        # Commit para salvar as mudanças no banco de dados
        db.session.commit()

        return jsonify(routine.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar a rotina: {e}")
        return jsonify({'error': str(e)}), 400


# DELETE (DELETE) - Deletar uma rotina pelo ID
@routine_bp.route('/<int:id>', methods=['DELETE'])
def delete_routine(id):
    routine = Routine.query.get_or_404(id)

    try:
        db.session.delete(routine)
        db.session.commit()
        logging.info(f"Rotina {routine.name} deletada com sucesso.")
        return jsonify({'message': 'Rotina deletada com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar a rotina: {e}")
        return jsonify({'error': str(e)}), 400
