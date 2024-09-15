from flask import Blueprint, request, jsonify
from models import db, Validation
import logging

validation_bp = Blueprint('validation_bp', __name__)

# CREATE (POST) - Criar uma nova validação
@validation_bp.route('/', methods=['POST'])
def create_validation():
    data = request.get_json()

    try:
        new_validation = Validation(
            field_id=data.get('field_id'),
            operator=data.get('operator'),
            compared_value=data.get('compared_value')
        )

        db.session.add(new_validation)
        db.session.commit()
        logging.info(f"Validação criada com sucesso: {new_validation.id}")
        return jsonify(new_validation.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar validação: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todas as validações
@validation_bp.route('/', methods=['GET'])
def get_all_validations():
    validations = Validation.query.all()
    return jsonify([validation.to_dict() for validation in validations]), 200

# READ (GET) - Obter uma validação específica por ID
@validation_bp.route('/<int:id>', methods=['GET'])
def get_validation(id):
    validation = Validation.query.get_or_404(id)
    return jsonify(validation.to_dict()), 200

# UPDATE (PUT) - Atualizar uma validação por ID
@validation_bp.route('/<int:id>', methods=['PUT'])
def update_validation(id):
    validation = Validation.query.get_or_404(id)
    data = request.get_json()

    try:
        validation.field_id = data.get('field_id', validation.field_id)
        validation.operator = data.get('operator', validation.operator)
        validation.compared_value = data.get('compared_value', validation.compared_value)

        db.session.commit()
        return jsonify(validation.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar a validação: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar uma validação por ID
@validation_bp.route('/<int:id>', methods=['DELETE'])
def delete_validation(id):
    validation = Validation.query.get_or_404(id)

    try:
        db.session.delete(validation)
        db.session.commit()
        logging.info(f"Validação {validation.id} deletada com sucesso.")
        return jsonify({'message': 'Validação deletada com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar validação: {e}")
        return jsonify({'error': str(e)}), 400
