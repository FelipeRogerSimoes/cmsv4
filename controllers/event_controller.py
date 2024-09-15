from flask import Blueprint, request, jsonify
from models import db, Event
import logging

event_bp = Blueprint('event_bp', __name__)

# CREATE (POST) - Criar um novo evento
@event_bp.route('/', methods=['POST'])
def create_event():
    data = request.get_json()

    try:
        # Criar um novo objeto Event
        new_event = Event(
            name=data.get('name'),
            type=data.get('type'),
            conditions=data.get('conditions')
        )

        # Adicionar à sessão do banco de dados
        db.session.add(new_event)
        db.session.commit()

        logging.info(f"Evento {new_event.name} criado com sucesso.")
        return jsonify(new_event.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar o evento: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todos os eventos
@event_bp.route('/', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events]), 200

# READ (GET) - Obter um evento específico pelo ID
@event_bp.route('/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get_or_404(id)
    return jsonify(event.to_dict()), 200

# UPDATE (PUT) - Atualizar um evento pelo ID
@event_bp.route('/<int:id>', methods=['PUT'])
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.get_json()

    try:
        # Atualizar apenas os campos que foram enviados
        event.name = data.get('name', event.name)
        event.type = data.get('type', event.type)
        event.conditions = data.get('conditions', event.conditions)

        # Commit para salvar as mudanças no banco de dados
        db.session.commit()

        return jsonify(event.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar o evento: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar um evento pelo ID
@event_bp.route('/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)

    try:
        db.session.delete(event)
        db.session.commit()
        logging.info(f"Evento {event.name} deletado com sucesso.")
        return jsonify({'message': 'Evento deletado com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar o evento: {e}")
        return jsonify({'error': str(e)}), 400
