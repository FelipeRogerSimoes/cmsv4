from flask import Blueprint, request, jsonify
from models import db, SystemUser
import logging

system_user_bp = Blueprint('system_user', __name__)

# CREATE (POST) - Criar um novo SystemUser
@system_user_bp.route('/', methods=['POST'])
def create_system_user():
    data = request.get_json()

    try:
        new_system_user = SystemUser(
            person_id=data.get('person_id'),
            manager=data.get('manager'),
            goal_type=data.get('goal_type'),
            job_title=data.get('job_title'),
            level=data.get('level'),
            collaborator_type=data.get('collaborator_type'),
            user_type=data.get('user_type'),
            username=data.get('username'),
            active=data.get('active', True)  # Por padrão, o usuário é ativo
        )

        db.session.add(new_system_user)
        db.session.commit()
        logging.info(f"Usuário do sistema criado com sucesso: {new_system_user.id}")
        return jsonify(new_system_user.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar usuário do sistema: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todos os SystemUsers
@system_user_bp.route('/', methods=['GET'])
def get_all_system_users():
    system_users = SystemUser.query.all()
    return jsonify([system_user.to_dict() for system_user in system_users]), 200

# READ (GET) - Obter um SystemUser específico por ID
@system_user_bp.route('/<int:id>', methods=['GET'])
def get_system_user(id):
    system_user = SystemUser.query.get_or_404(id)
    return jsonify(system_user.to_dict()), 200

# UPDATE (PUT) - Atualizar um SystemUser por ID
@system_user_bp.route('/<int:id>', methods=['PUT'])
def update_system_user(id):
    system_user = SystemUser.query.get_or_404(id)
    data = request.get_json()

    try:
        system_user.person_id = data.get('person_id', system_user.person_id)
        system_user.manager = data.get('manager', system_user.manager)
        system_user.goal_type = data.get('goal_type', system_user.goal_type)
        system_user.job_title = data.get('job_title', system_user.job_title)
        system_user.level = data.get('level', system_user.level)
        system_user.collaborator_type = data.get('collaborator_type', system_user.collaborator_type)
        system_user.user_type = data.get('user_type', system_user.user_type)
        system_user.username = data.get('username', system_user.username)
        system_user.active = data.get('active', system_user.active)

        db.session.commit()
        return jsonify(system_user.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar usuário do sistema: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar um SystemUser por ID
@system_user_bp.route('/<int:id>', methods=['DELETE'])
def delete_system_user(id):
    system_user = SystemUser.query.get_or_404(id)

    try:
        db.session.delete(system_user)
        db.session.commit()
        logging.info(f"Usuário do sistema {system_user.id} deletado com sucesso.")
        return jsonify({'message': 'Usuário do sistema deletado com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar usuário do sistema: {e}")
        return jsonify({'error': str(e)}), 400
