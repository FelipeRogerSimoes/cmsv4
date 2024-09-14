from flask import Blueprint, render_template

# Definindo o blueprint para o gráfico de timesheets
graph_timesheets_bp = Blueprint('graph_timesheets_bp', __name__)


# Endpoint para servir o gráfico de timesheets
@graph_timesheets_bp.route('/timesheets_chart')
def timesheets_chart():
    # Dados fictícios de exemplo (substitua pelos dados reais do banco de dados)
    timesheets_data = [
        {'activity': 'Análise de sistema', 'hours': 8},
        {'activity': 'Reunião com cliente', 'hours': 2},
        {'activity': 'Desenvolvimento de relatórios', 'hours': 5}
    ]

    # Renderizar o template HTML que contém o gráfico
    return render_template('timesheets_chart.html', timesheets=timesheets_data)
