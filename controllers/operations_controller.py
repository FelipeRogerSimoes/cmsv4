from flask import Blueprint, request, jsonify
from models import db, Operations
import logging

operations_bp = Blueprint('operations', __name__)

# CREATE (POST) - Criar uma nova operação
@operations_bp.route('/', methods=['POST'])
def create_operation():
    data = request.get_json()

    try:
        new_operation = Operations(
            name=data.get('name'),
            responsible=data.get('responsible'),
            group_name=data.get('group_name'),
            director=data.get('director')
        )

        db.session.add(new_operation)
        db.session.commit()
        logging.info(f"Operação criada com sucesso: {new_operation.id}")
        return jsonify(new_operation.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar operação: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todas as operações
@operations_bp.route('/', methods=['GET'])
def get_all_operations():
    operations = Operations.query.all()
    return jsonify([operation.to_dict() for operation in operations]), 200

# READ (GET) - Obter uma operação específica por ID
@operations_bp.route('/<int:id>', methods=['GET'])
def get_operation(id):
    operation = Operations.query.get_or_404(id)
    return jsonify(operation.to_dict()), 200

# UPDATE (PUT) - Atualizar uma operação por ID
@operations_bp.route('/<int:id>', methods=['PUT'])
def update_operation(id):
    operation = Operations.query.get_or_404(id)
    data = request.get_json()

    try:
        operation.name = data.get('name', operation.name)
        operation.responsible = data.get('responsible', operation.responsible)
        operation.group_name = data.get('group_name', operation.group_name)
        operation.director = data.get('director', operation.director)

        db.session.commit()
        return jsonify(operation.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar operação: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar uma operação por ID
@operations_bp.route('/<int:id>', methods=['DELETE'])
def delete_operation(id):
    operation = Operations.query.get_or_404(id)

    try:
        db.session.delete(operation)
        db.session.commit()
        logging.info(f"Operação {operation.id} deletada com sucesso.")
        return jsonify({'message': 'Operação deletada com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar operação: {e}")
        return jsonify({'error': str(e)}), 400
