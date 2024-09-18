from flask import Blueprint, request, jsonify
from models import db, UserGoal, UserLeave, Holiday, SystemUser
from datetime import timedelta, date, datetime
import calendar

goals_bp = Blueprint('goals_bp', __name__)

# Endpoint para adicionar uma nova ausência (leave)
@goals_bp.route('/add_leave', methods=['POST'])
def add_leave():
    data = request.get_json()
    try:
        # Converter as datas de string para objeto date do Python
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

        user_leave = UserLeave(
            user_id=data['user_id'],
            start_date=start_date,  # Usar o objeto de data convertido
            end_date=end_date,  # Usar o objeto de data convertido
            leave_type=data['leave_type']
        )

        db.session.add(user_leave)
        db.session.commit()

        return jsonify({'message': 'Registro de ausência adicionado!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
# Endpoint para adicionar um feriado
@goals_bp.route('/add_holiday', methods=['POST'])
def add_holiday():
    data = request.get_json()
    try:
        holiday = Holiday(date=data['date'], name=data.get('name'))
        db.session.add(holiday)
        db.session.commit()
        return jsonify({'message': 'Feriado registrado com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Endpoint para registrar uma nova meta (incluindo valor e horas por dia)
@goals_bp.route('/add_goal', methods=['POST'])
def add_goal():
    data = request.get_json()

    try:
        # Registrar a meta
        user_goal = UserGoal(
            user_id=data['user_id'],
            goal_value=data['goal_value'],  # Meta total financeira no mês
            goal_hour=data['goal_hour'],    # Horas esperadas por dia
            month=data['month'],
            year=data['year']
        )
        db.session.add(user_goal)
        db.session.commit()

        return jsonify({'message': 'Meta registrada com sucesso!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Função para calcular dias úteis
def get_working_days(user_id, year, month):
    first_day, last_day = calendar.monthrange(year, month)
    days_in_month = [date(year, month, day) for day in range(1, last_day + 1)]

    weekdays = [d for d in days_in_month if d.weekday() < 5]  # Seg-Sex

    # Filtrar feriados
    holidays = Holiday.query.filter(Holiday.date.in_(weekdays)).all()
    weekdays = [d for d in weekdays if d not in [h.date for h in holidays]]

    # Filtrar atestados ou férias do usuário
    leaves = UserLeave.query.filter(
        UserLeave.user_id == user_id,
        UserLeave.start_date <= days_in_month[-1],
        UserLeave.end_date >= days_in_month[0]
    ).all()

    for leave in leaves:
        leave_range = [leave.start_date + timedelta(days=i) for i in range((leave.end_date - leave.start_date).days + 1)]
        weekdays = [d for d in weekdays if d not in leave_range]

    return weekdays

# Distribuir metas diárias com base no valor financeiro
def distribute_goal(user_id, year, month, total_goal_value, daily_goal_hours):
    working_days = get_working_days(user_id, year, month)
    daily_goal_value = total_goal_value / len(working_days) if working_days else 0
    return {day: {'goal_value': daily_goal_value, 'goal_hours': daily_goal_hours} for day in working_days}

# Endpoint para consultar metas diárias (valor e horas por dia)
@goals_bp.route('/user_goal/<int:user_id>/<int:year>/<int:month>', methods=['GET'])
def get_user_goal(user_id, year, month):
    user_goal = UserGoal.query.filter_by(user_id=user_id, year=year, month=month).first()
    if user_goal:
        distributed_goal = distribute_goal(user_id, year, month, user_goal.goal_value, user_goal.goal_hour)
        return jsonify(distributed_goal), 200
    return jsonify({'error': 'Meta não encontrada!'}), 404
