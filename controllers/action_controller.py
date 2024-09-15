from flask import Blueprint, request, jsonify
from models import db, Action
import logging

action_bp = Blueprint('action_bp', __name__)

# CREATE (POST) - Criar uma nova ação
@action_bp.route('/', methods=['POST'])
def create_action():
    data = request.get_json()

    try:
        # Criar um novo objeto Action
        new_action = Action(
            name=data.get('name'),
            description=data.get('description'),
            function_name=data.get('function_name')
        )

        # Adicionar à sessão do banco de dados
        db.session.add(new_action)
        db.session.commit()

        logging.info(f"Ação {new_action.name} criada com sucesso.")
        return jsonify(new_action.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar a ação: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todas as ações
@action_bp.route('/', methods=['GET'])
def get_all_actions():
    actions = Action.query.all()
    return jsonify([action.to_dict() for action in actions]), 200

# READ (GET) - Obter uma ação específica pelo ID
@action_bp.route('/<int:id>', methods=['GET'])
def get_action(id):
    action = Action.query.get_or_404(id)
    return jsonify(action.to_dict()), 200

# UPDATE (PUT) - Atualizar uma ação pelo ID
@action_bp.route('/<int:id>', methods=['PUT'])
def update_action(id):
    action = Action.query.get_or_404(id)
    data = request.get_json()

    try:
        # Atualizar apenas os campos que foram enviados
        action.name = data.get('name', action.name)
        action.description = data.get('description', action.description)
        action.function_name = data.get('function_name', action.function_name)

        # Commit para salvar as mudanças no banco de dados
        db.session.commit()

        return jsonify(action.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar a ação: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar uma ação pelo ID
@action_bp.route('/<int:id>', methods=['DELETE'])
def delete_action(id):
    action = Action.query.get_or_404(id)

    try:
        db.session.delete(action)
        db.session.commit()
        logging.info(f"Ação {action.name} deletada com sucesso.")
        return jsonify({'message': 'Ação deletada com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar a ação: {e}")
        return jsonify({'error': str(e)}), 400
