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
        cpf_cnpj=data.get('cpf_cnpj')
    )

    logging.info(f"Novo objeto Person: {new_person}")

    # Adicionar o novo objeto à sessão
    db.session.add(new_person)
    logging.info("Objeto Person adicionado à sessão")

    try:
        # Commit para salvar no banco de dados
        db.session.commit()
        logging.info(f"Pessoa criada com sucesso com ID {new_person.id}")

    except Exception as e:
        db.session.rollback()  # Desfazer a transação em caso de erro
        logging.error(f"Erro ao salvar a pessoa: {e}")
        return jsonify({'error': str(e)}), 400

    # Verificar se o ID foi gerado e se o objeto ainda está presente
    if not new_person.id:
        logging.error("Erro: o ID da pessoa não foi gerado após o commit")
        return jsonify({'error': 'ID não gerado'}), 500

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
