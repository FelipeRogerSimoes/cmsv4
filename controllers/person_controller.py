from flask import Blueprint, request, jsonify
from models import db, Person
import logging

person_bp = Blueprint('person', __name__)

# CREATE (POST)
@person_bp.route('/', methods=['POST'])
def create_person():
    data = request.get_json()

    # Criar um novo objeto Person
    new_person = Person(
        name=data.get('name'),
        type=data.get('type'),
        cpf_cnpj=data.get('cpf_cnpj'),
        email=data.get('email'),
        whatsapp=data.get('whatsapp'),
        role=data.get('role', 'user'),  # Papel do usuário, padrão 'user'
        address=data.get('address'),
        deleted=False  # Padrão para False
    )

    db.session.add(new_person)

    try:
        db.session.commit()
        logging.info(f"Pessoa criada com sucesso com ID {new_person.id}")

    except Exception as e:
        db.session.rollback()  # Desfazer a transação em caso de erro
        logging.error(f"Erro ao salvar a pessoa: {e}")
        return jsonify({'error': str(e)}), 400

    return jsonify(new_person.to_dict()), 201


# Listar todas as pessoas (GET)
@person_bp.route('/', methods=['GET'])
def get_all_persons():
    persons = Person.query.filter_by(deleted=False).all()  # Listar apenas pessoas não deletadas logicamente
    return jsonify([person.to_dict() for person in persons]), 200


# Obter uma pessoa específica pelo ID (GET)
@person_bp.route('/<int:id>', methods=['GET'])
def get_person(id):
    person = Person.query.filter_by(id=id, deleted=False).first_or_404()  # Excluir logicamente deletados da busca
    return jsonify(person.to_dict()), 200


# Atualizar uma pessoa pelo ID (PUT)
@person_bp.route('/<int:id>', methods=['PUT'])
def update_person(id):
    person = Person.query.filter_by(id=id, deleted=False).first_or_404()  # Apenas pessoas não deletadas
    data = request.get_json()

    # Atualizar apenas os campos que foram enviados
    person.name = data.get('name', person.name)
    person.type = data.get('type', person.type)
    person.cpf_cnpj = data.get('cpf_cnpj', person.cpf_cnpj)
    person.email = data.get('email', person.email)
    person.whatsapp = data.get('whatsapp', person.whatsapp)
    person.role = data.get('role', person.role)
    person.address = data.get('address', person.address)

    db.session.commit()

    return jsonify(person.to_dict()), 200


# Deletar logicamente uma pessoa pelo ID (DELETE)
@person_bp.route('/<int:id>', methods=['DELETE'])
def soft_delete_person(id):
    person = Person.query.filter_by(id=id, deleted=False).first_or_404()

    # Exclusão lógica
    person.deleted = True

    db.session.commit()

    return jsonify({'message': 'Pessoa marcada como deletada.'}), 200
