from flask import Blueprint, request, jsonify
from models import db, Cases
from business_rules import validate_case  # Certifique-se de que essa linha esteja correta

cases_bp = Blueprint('cases_bp', __name__)


@cases_bp.route('/', methods=['POST'])
def create_case():
    data = request.get_json()

    # Validação de regras de negócio para criação de casos
    is_valid, message = validate_case(data)
    if not is_valid:
        return jsonify({'error': message}), 400

    new_case = Cases(
        description=data['description'],
        entry_date=data['entry_date'],
        status=data['status'],
        insurance_company_id=data['insurance_company_id'],
        rate2=data.get('rate2', False),
        fee_limit=data.get('fee_limit'),
        legal_action=data.get('legal_action', False),
        damage_estimate=data.get('damage_estimate', 0),
        insured_name=data['insured_name'],
        condition=data['condition'],
        auxiliary_adjuster=data.get('auxiliary_adjuster'),
        lead_adjuster=data.get('lead_adjuster'),
        operation_id=data['operation_id'],
        internal_number=data['internal_number']
    )

    db.session.add(new_case)
    db.session.commit()
    return jsonify(new_case.to_dict()), 201
