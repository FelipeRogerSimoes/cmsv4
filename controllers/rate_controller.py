from flask import Blueprint, request, jsonify
from models import db, Rate
import logging

rate_bp = Blueprint('rate_bp', __name__)

# CREATE (POST) - Criar uma nova rate
@rate_bp.route('/', methods=['POST'])
def create_rate():
    data = request.get_json()

    try:
        new_rate = Rate(
            parameter_id=data.get('parameter_id'),
            value=data.get('value'),
            type=data.get('type'),
            billing_type=data.get('billing_type')
        )

        db.session.add(new_rate)
        db.session.commit()
        logging.info(f"Rate criada com sucesso: {new_rate.id}")
        return jsonify(new_rate.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar rate: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todas as rates
@rate_bp.route('/', methods=['GET'])
def get_all_rates():
    rates = Rate.query.all()
    return jsonify([rate.to_dict() for rate in rates]), 200

# READ (GET) - Obter uma rate específica por ID
@rate_bp.route('/<int:id>', methods=['GET'])
def get_rate(id):
    rate = Rate.query.get_or_404(id)
    return jsonify(rate.to_dict()), 200

# UPDATE (PUT) - Atualizar uma rate pelo ID
@rate_bp.route('/<int:id>', methods=['PUT'])
def update_rate(id):
    rate = Rate.query.get_or_404(id)
    data = request.get_json()

    try:
        rate.parameter_id = data.get('parameter_id', rate.parameter_id)
        rate.value = data.get('value', rate.value)
        rate.type = data.get('type', rate.type)
        rate.billing_type = data.get('billing_type', rate.billing_type)

        db.session.commit()
        return jsonify(rate.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar rate: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar uma rate pelo ID
@rate_bp.route('/<int:id>', methods=['DELETE'])
def delete_rate(id):
    rate = Rate.query.get_or_404(id)

    try:
        db.session.delete(rate)
        db.session.commit()
        logging.info(f"Rate {rate.id} deletada com sucesso.")
        return jsonify({'message': 'Rate deletada com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar rate: {e}")
        return jsonify({'error': str(e)}), 400
