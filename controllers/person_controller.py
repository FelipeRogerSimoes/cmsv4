from flask import Blueprint, request, jsonify
from models import db, Person

person_bp = Blueprint('person_bp', __name__)


# 1. Criar uma nova pessoa (POST)
@person_bp.route('/', methods=['POST'])
def create_person():
    data = request.get_json()

    # Verificar se todos os campos necessários estão presentes
    if not all(k in data for k in ('name', 'type', 'cpf_cnpj')):
        return jsonify({'error': 'Nome, tipo e CPF/CNPJ são obrigatórios.'}), 400

    # Verificar se CPF/CNPJ já existe
    existing_person = Person.query.filter_by(cpf_cnpj=data['cpf_cnpj']).first()
    if existing_person:
        return jsonify({'error': 'Uma pessoa com este CPF/CNPJ já existe.'}), 400

    # Criar nova pessoa
    new_person = Person(
        name=data['name'],
        type=data['type'],
        cpf_cnpj=data['cpf_cnpj']
    )

    db.session.add(new_person)
    db.session.commit()

    return jsonify(new_person.to_dict()), 201


# 2. Listar todas as pessoas (GET)
@person_bp.route('/', methods=['GET'])
def get_all_persons():
    persons = Person.query.all()
    return jsonify([person.to_dict() for person in persons]), 200


# 3. Obter uma pessoa específica pelo ID (GET)
@person_bp.route('/<int:id>', methods=['GET'])
def get_person(id):
    person = Person.query.get_or_404(id)
    return jsonify(person.to_dict()), 200


# 4. Atualizar uma pessoa pelo ID (PUT)
@person_bp.route('/<int:id>', methods=['PUT'])
def update_person(id):
    person = Person.query.get_or_404(id)
    data = request.get_json()

    # Atualizar apenas os campos que foram enviados
    person.name = data.get('name', person.name)
    person.type = data.get('type', person.type)
    person.cpf_cnpj = data.get('cpf_cnpj', person.cpf_cnpj)

    db.session.commit()

    return jsonify(person.to_dict()), 200


# 5. Deletar uma pessoa pelo ID (DELETE)
@person_bp.route('/<int:id>', methods=['DELETE'])
def delete_person(id):
    person = Person.query.get_or_404(id)

    db.session.delete(person)
    db.session.commit()

    return jsonify({'message': 'Pessoa deletada com sucesso.'}), 200
