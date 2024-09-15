from flask import Blueprint, request, jsonify
from models import db, InsuranceCompany
import logging

insurance_company_bp = Blueprint('insurance_company_bp', __name__)

# CREATE (POST) - Criar uma nova companhia de seguros
@insurance_company_bp.route('/', methods=['POST'])
def create_insurance_company():
    data = request.get_json()

    try:
        new_insurance_company = InsuranceCompany(
            person_id=data.get('person_id')
        )

        db.session.add(new_insurance_company)
        db.session.commit()
        logging.info(f"Companhia de seguros criada com sucesso: {new_insurance_company.id}")
        return jsonify(new_insurance_company.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar companhia de seguros: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todas as companhias de seguros
@insurance_company_bp.route('/', methods=['GET'])
def get_all_insurance_companies():
    insurance_companies = InsuranceCompany.query.all()
    return jsonify([insurance_company.to_dict() for insurance_company in insurance_companies]), 200

# READ (GET) - Obter uma companhia de seguros específica por ID
@insurance_company_bp.route('/<int:id>', methods=['GET'])
def get_insurance_company(id):
    insurance_company = InsuranceCompany.query.get_or_404(id)
    return jsonify(insurance_company.to_dict()), 200

# UPDATE (PUT) - Atualizar uma companhia de seguros por ID
@insurance_company_bp.route('/<int:id>', methods=['PUT'])
def update_insurance_company(id):
    insurance_company = InsuranceCompany.query.get_or_404(id)
    data = request.get_json()

    try:
        insurance_company.person_id = data.get('person_id', insurance_company.person_id)

        db.session.commit()
        return jsonify(insurance_company.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar companhia de seguros: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar uma companhia de seguros por ID
@insurance_company_bp.route('/<int:id>', methods=['DELETE'])
def delete_insurance_company(id):
    insurance_company = InsuranceCompany.query.get_or_404(id)

    try:
        db.session.delete(insurance_company)
        db.session.commit()
        logging.info(f"Companhia de seguros {insurance_company.id} deletada com sucesso.")
        return jsonify({'message': 'Companhia de seguros deletada com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar companhia de seguros: {e}")
        return jsonify({'error': str(e)}), 400
