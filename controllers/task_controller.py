from flask import Blueprint, request, jsonify
from models import db, Task
import logging
from datetime import datetime

task_bp = Blueprint('task_bp', __name__)

# CREATE (POST) - Criar uma nova tarefa
@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()

    try:
        # Converter datas para objetos datetime
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        conclusion_date = datetime.strptime(data.get('conclusion_date'), '%Y-%m-%d').date() if data.get('conclusion_date') else None
        due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d').date() if data.get('due_date') else None

        # Criar um novo objeto Task
        new_task = Task(
            routine_id=data.get('routine_id'),
            action=data.get('action'),
            name=data.get('name'),
            start_date=start_date,
            conclusion_date=conclusion_date,
            due_date=due_date,
            document_id=data.get('document_id'),
            mandatory=data.get('mandatory'),
            SLA=data.get('SLA'),
            responsible=data.get('responsible'),
            status=data.get('status'),
            condition=data.get('condition')
        )

        # Adicionar à sessão do banco de dados
        db.session.add(new_task)
        db.session.commit()

        logging.info(f"Tarefa {new_task.name} criada com sucesso.")
        return jsonify(new_task.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar a tarefa: {e}")
        return jsonify({'error': str(e)}), 400


# READ (GET) - Obter todas as tarefas
@task_bp.route('/', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200


# READ (GET) - Obter uma tarefa específica pelo ID
@task_bp.route('/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict()), 200


# UPDATE (PUT) - Atualizar uma tarefa pelo ID
@task_bp.route('/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    try:
        # Atualizar apenas os campos que foram enviados
        task.routine_id = data.get('routine_id', task.routine_id)
        task.action = data.get('action', task.action)
        task.name = data.get('name', task.name)
        task.document_id = data.get('document_id', task.document_id)
        task.mandatory = data.get('mandatory', task.mandatory)
        task.SLA = data.get('SLA', task.SLA)
        task.responsible = data.get('responsible', task.responsible)
        task.status = data.get('status', task.status)
        task.condition = data.get('condition', task.condition)

        # Converter e atualizar as datas
        if 'start_date' in data:
            task.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'conclusion_date' in data:
            task.conclusion_date = datetime.strptime(data['conclusion_date'], '%Y-%m-%d').date()
        if 'due_date' in data:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()

        # Commit para salvar as mudanças no banco de dados
        db.session.commit()

        return jsonify(task.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar a tarefa: {e}")
        return jsonify({'error': str(e)}), 400


# DELETE (DELETE) - Deletar uma tarefa pelo ID
@task_bp.route('/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        logging.info(f"Tarefa {task.name} deletada com sucesso.")
        return jsonify({'message': 'Tarefa deletada com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar a tarefa: {e}")
        return jsonify({'error': str(e)}), 400
