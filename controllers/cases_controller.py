from flask import Blueprint, request, jsonify
from models import db, Case
import logging
from datetime import datetime

cases_bp = Blueprint('cases', __name__)

# CREATE (POST) - Criar um novo caso
@cases_bp.route('/', methods=['POST'])
def create_case():
    data = request.get_json()

    try:
        # Converta as datas no formato string para objetos de data do Python
        entry_date = datetime.strptime(data.get('entry_date'), '%Y-%m-%d').date() if data.get('entry_date') else None
        loss_date = datetime.strptime(data.get('loss_date'), '%Y-%m-%d').date() if data.get('loss_date') else None
        notification_date = datetime.strptime(data.get('notification_date'), '%Y-%m-%d').date() if data.get('notification_date') else None

        new_case = Case(
            description=data.get('description'),
            judicial_action=data.get('judicial_action'),
            policy_number=data.get('policy_number'),
            reported_to_insurer=data.get('reported_to_insurer'),
            case_name=data.get('case_name'),
            case_number=data.get('case_number'),
            condition=data.get('condition'),
            broker=data.get('broker'),
            entry_date=entry_date,  # Usar objeto date
            loss_date=loss_date,  # Usar objeto date
            notification_date=notification_date,  # Usar objeto date
            fee_estimate=data.get('fee_estimate'),
            damage_estimate=data.get('damage_estimate'),
            salvage_estimate=data.get('salvage_estimate'),
            excluded=data.get('excluded'),
            fee_limit=data.get('fee_limit'),
            incident_location=data.get('incident_location'),
            operation_id=data.get('operation_id'),
            rate_2=data.get('rate_2'),
            insurer_reference=data.get('insurer_reference'),
            lead_adjuster=data.get('lead_adjuster'),
            auxiliary_adjuster=data.get('auxiliary_adjuster'),
            reserve=data.get('reserve'),
            salvage=data.get('salvage'),
            search=data.get('search'),
            insured_name=data.get('insured_name'),
            insurer_id=data.get('insurer_id'),
            status=data.get('status'),
            temporal=data.get('temporal'),
            billing_type=data.get('billing_type'),
            fee_limit_value=data.get('fee_limit_value'),
            physical_inspection=data.get('physical_inspection')
        )

        db.session.add(new_case)
        db.session.commit()
        logging.info(f"Caso criado com sucesso: {new_case.id}")
        return jsonify(new_case.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar caso: {e}")
        return jsonify({'error': str(e)}), 400


@cases_bp.route('/', methods=['GET'])
def get_all_cases():
    cases = Case.query.all()
    return jsonify([case.to_dict() for case in cases]), 200

@cases_bp.route('/<int:id>', methods=['GET'])
def get_case(id):
    case = Case.query.get_or_404(id)
    return jsonify(case.to_dict()), 200

@cases_bp.route('/<int:id>', methods=['PUT'])
def update_case(id):
    case = Case.query.get_or_404(id)
    data = request.get_json()

    try:
        # Converta as datas no formato string para objetos de data do Python
        entry_date = datetime.strptime(data.get('entry_date'), '%Y-%m-%d').date() if data.get('entry_date') else None
        loss_date = datetime.strptime(data.get('loss_date'), '%Y-%m-%d').date() if data.get('loss_date') else None
        notification_date = datetime.strptime(data.get('notification_date'), '%Y-%m-%d').date() if data.get('notification_date') else None

        # Atualizar apenas os campos que foram enviados
        case.description = data.get('description', case.description)
        case.judicial_action = data.get('judicial_action', case.judicial_action)
        case.policy_number = data.get('policy_number', case.policy_number)
        case.reported_to_insurer = data.get('reported_to_insurer', case.reported_to_insurer)
        case.case_name = data.get('case_name', case.case_name)
        case.case_number = data.get('case_number', case.case_number)
        case.condition = data.get('condition', case.condition)
        case.broker = data.get('broker', case.broker)
        case.entry_date = entry_date or case.entry_date
        case.loss_date = loss_date or case.loss_date
        case.notification_date = notification_date or case.notification_date
        case.fee_estimate = data.get('fee_estimate', case.fee_estimate)
        case.damage_estimate = data.get('damage_estimate', case.damage_estimate)
        case.salvage_estimate = data.get('salvage_estimate', case.salvage_estimate)
        case.excluded = data.get('excluded', case.excluded)
        case.fee_limit = data.get('fee_limit', case.fee_limit)
        case.incident_location = data.get('incident_location', case.incident_location)
        case.operation_id = data.get('operation_id', case.operation_id)
        case.rate_2 = data.get('rate_2', case.rate_2)
        case.insurer_reference = data.get('insurer_reference', case.insurer_reference)
        case.lead_adjuster = data.get('lead_adjuster', case.lead_adjuster)
        case.auxiliary_adjuster = data.get('auxiliary_adjuster', case.auxiliary_adjuster)
        case.reserve = data.get('reserve', case.reserve)
        case.salvage = data.get('salvage', case.salvage)
        case.search = data.get('search', case.search)
        case.insured_name = data.get('insured_name', case.insured_name)
        case.insurer_id = data.get('insurer_id', case.insurer_id)
        case.status = data.get('status', case.status)
        case.temporal = data.get('temporal', case.temporal)
        case.billing_type = data.get('billing_type', case.billing_type)
        case.fee_limit_value = data.get('fee_limit_value', case.fee_limit_value)
        case.physical_inspection = data.get('physical_inspection', case.physical_inspection)

        db.session.commit()
        return jsonify(case.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar caso: {e}")
        return jsonify({'error': str(e)}), 400


@cases_bp.route('/<int:id>', methods=['DELETE'])
def delete_case(id):
    case = Case.query.get_or_404(id)

    try:
        db.session.delete(case)
        db.session.commit()
        logging.info(f"Caso {case.id} deletado com sucesso.")
        return jsonify({'message': 'Caso deletado com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar caso: {e}")
        return jsonify({'error': str(e)}), 400


