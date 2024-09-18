from flask import Flask, render_template
import os

app = Flask(__name__)

# Define a rota para servir o HTML de teste
@app.route('/')
def render_chart():
    return render_template('chart_test.html')  # Certifique-se de ter esse arquivo HTML

if __name__ == '__main__':
    # Define o caminho para os templates
    template_dir = os.path.abspath('path_to_your_templates_directory')
    app.template_folder = template_dir
    app.run(debug=True)
