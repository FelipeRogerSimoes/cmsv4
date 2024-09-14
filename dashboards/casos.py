from flask import Blueprint, render_template

# Definir o blueprint para casos
casos_bp = Blueprint('casos_bp', __name__)


# Rota para o dashboard de casos
@casos_bp.route('/')
def casos_dashboard():
    # Dados fictícios ou lógica que você queira adicionar
    casos_data = [
        {'id': 101, 'description': 'Insurance claim for car accident', 'status': 'Open'},
        {'id': 102, 'description': 'Fire damage claim', 'status': 'Closed'},
        {'id': 103, 'description': 'Health insurance claim', 'status': 'Pending'}
    ]

    # Renderizar o template HTML e passar os dados
    return render_template('casos.html', casos=casos_data)
