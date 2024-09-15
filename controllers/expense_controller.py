from flask import Blueprint, request, jsonify
from models import db, Expense
import logging
from datetime import datetime

expense_bp = Blueprint('expense_bp', __name__)

# Função auxiliar para converter string para date
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

# CREATE (POST) - Criar um novo expense
@expense_bp.route('/', methods=['POST'])
def create_expense():
    data = request.get_json()

    try:
        # Converter a data de despesa
        expense_date = parse_date(data.get('expense_date'))
        if not expense_date:
            return jsonify({'error': 'Data de despesa inválida. Use o formato YYYY-MM-DD.'}), 400

        # Criar um novo objeto Expense
        new_expense = Expense(
            case_id=data.get('case_id'),
            rate_limit=data.get('rate_limit'),
            declared_value=data.get('declared_value'),
            expense_type=data.get('expense_type'),
            expense_date=expense_date,
            receipt_link=data.get('receipt_link'),
            reimbursable=data.get('reimbursable'),
            adjuster=data.get('adjuster')
        )

        # Adicionar à sessão do banco de dados
        db.session.add(new_expense)
        db.session.commit()

        logging.info(f"Despesa criada com sucesso.")
        return jsonify(new_expense.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar a despesa: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todas as despesas
@expense_bp.route('/', methods=['GET'])
def get_all_expenses():
    expenses = Expense.query.all()
    return jsonify([expense.to_dict() for expense in expenses]), 200

# READ (GET) - Obter uma despesa específica pelo ID
@expense_bp.route('/<int:id>', methods=['GET'])
def get_expense(id):
    expense = Expense.query.get_or_404(id)
    return jsonify(expense.to_dict()), 200

# UPDATE (PUT) - Atualizar uma despesa pelo ID
@expense_bp.route('/<int:id>', methods=['PUT'])
def update_expense(id):
    expense = Expense.query.get_or_404(id)
    data = request.get_json()

    try:
        # Converter a data de despesa
        expense_date = parse_date(data.get('expense_date'))
        if not expense_date:
            return jsonify({'error': 'Data de despesa inválida. Use o formato YYYY-MM-DD.'}), 400

        # Atualizar apenas os campos que foram enviados
        expense.case_id = data.get('case_id', expense.case_id)
        expense.rate_limit = data.get('rate_limit', expense.rate_limit)
        expense.declared_value = data.get('declared_value', expense.declared_value)
        expense.expense_type = data.get('expense_type', expense.expense_type)
        expense.expense_date = expense_date
        expense.receipt_link = data.get('receipt_link', expense.receipt_link)
        expense.reimbursable = data.get('reimbursable', expense.reimbursable)
        expense.adjuster = data.get('adjuster', expense.adjuster)

        # Commit para salvar as mudanças no banco de dados
        db.session.commit()

        return jsonify(expense.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar a despesa: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar uma despesa pelo ID
@expense_bp.route('/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)

    try:
        db.session.delete(expense)
        db.session.commit()
        logging.info(f"Despesa deletada com sucesso.")
        return jsonify({'message': 'Despesa deletada com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar a despesa: {e}")
        return jsonify({'error': str(e)}), 400
