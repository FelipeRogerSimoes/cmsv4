from flask import Blueprint, request, jsonify
from models import db, Field
import logging

field_bp = Blueprint('field_bp', __name__)

# CREATE (POST) - Criar um novo campo
@field_bp.route('/', methods=['POST'])
def create_field():
    data = request.get_json()

    try:
        new_field = Field(
            name=data.get('name'),
            description=data.get('description'),
            sql_query=data.get('sql_query')
        )

        db.session.add(new_field)
        db.session.commit()
        logging.info(f"Campo {new_field.name} criado com sucesso.")
        return jsonify(new_field.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar o campo: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todos os campos
@field_bp.route('/', methods=['GET'])
def get_all_fields():
    fields = Field.query.all()
    return jsonify([field.to_dict() for field in fields]), 200

# READ (GET) - Obter um campo específico por ID
@field_bp.route('/<int:id>', methods=['GET'])
def get_field(id):
    field = Field.query.get_or_404(id)
    return jsonify(field.to_dict()), 200

# UPDATE (PUT) - Atualizar um campo por ID
@field_bp.route('/<int:id>', methods=['PUT'])
def update_field(id):
    field = Field.query.get_or_404(id)
    data = request.get_json()

    try:
        field.name = data.get('name', field.name)
        field.description = data.get('description', field.description)
        field.sql_query = data.get('sql_query', field.sql_query)

        db.session.commit()
        return jsonify(field.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar o campo: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar um campo por ID
@field_bp.route('/<int:id>', methods=['DELETE'])
def delete_field(id):
    field = Field.query.get_or_404(id)

    try:
        db.session.delete(field)
        db.session.commit()
        logging.info(f"Campo {field.name} deletado com sucesso.")
        return jsonify({'message': 'Campo deletado com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar o campo: {e}")
        return jsonify({'error': str(e)}), 400
