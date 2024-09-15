from flask import Blueprint, request, jsonify
from models import db, Parameter
import logging

parameter_bp = Blueprint('parameter_bp', __name__)

# CREATE (POST) - Criar um novo parâmetro
@parameter_bp.route('/', methods=['POST'])
def create_parameter():
    data = request.get_json()

    try:
        # Criar um novo objeto Parameter
        new_parameter = Parameter(
            name=data.get('name'),
            operator=data.get('operator'),
            validation_id=data.get('validation_id'),
            sequence=data.get('sequence')
        )

        # Adicionar à sessão do banco de dados
        db.session.add(new_parameter)
        db.session.commit()

        logging.info(f"Parâmetro {new_parameter.name} criado com sucesso.")
        return jsonify(new_parameter.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar o parâmetro: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todos os parâmetros
@parameter_bp.route('/', methods=['GET'])
def get_all_parameters():
    parameters = Parameter.query.all()
    return jsonify([parameter.to_dict() for parameter in parameters]), 200

# READ (GET) - Obter um parâmetro específico pelo ID
@parameter_bp.route('/<int:id>', methods=['GET'])
def get_parameter(id):
    parameter = Parameter.query.get_or_404(id)
    return jsonify(parameter.to_dict()), 200

# UPDATE (PUT) - Atualizar um parâmetro pelo ID
@parameter_bp.route('/<int:id>', methods=['PUT'])
def update_parameter(id):
    parameter = Parameter.query.get_or_404(id)
    data = request.get_json()

    try:
        # Atualizar apenas os campos que foram enviados
        parameter.name = data.get('name', parameter.name)
        parameter.operator = data.get('operator', parameter.operator)
        parameter.validation_id = data.get('validation_id', parameter.validation_id)
        parameter.sequence = data.get('sequence', parameter.sequence)

        # Commit para salvar as mudanças no banco de dados
        db.session.commit()

        return jsonify(parameter.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar o parâmetro: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar um parâmetro pelo ID
@parameter_bp.route('/<int:id>', methods=['DELETE'])
def delete_parameter(id):
    parameter = Parameter.query.get_or_404(id)

    try:
        db.session.delete(parameter)
        db.session.commit()
        logging.info(f"Parâmetro {parameter.name} deletado com sucesso.")
        return jsonify({'message': 'Parâmetro deletado com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar o parâmetro: {e}")
        return jsonify({'error': str(e)}), 400
