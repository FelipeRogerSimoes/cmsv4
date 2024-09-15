from flask import Blueprint, request, jsonify
from models import db, Document
import logging

document_bp = Blueprint('document_bp', __name__)

# CREATE (POST) - Criar um novo documento
@document_bp.route('/', methods=['POST'])
def create_document():
    data = request.get_json()

    try:
        # Criar um novo objeto Document
        new_document = Document(
            file=data.get('file'),
            description=data.get('description'),
            stage=data.get('stage'),
            related_stage=data.get('related_stage'),
            name=data.get('name'),
            temporal=data.get('temporal'),
            document_type=data.get('document_type')
        )

        # Adicionar à sessão do banco de dados
        db.session.add(new_document)
        db.session.commit()

        logging.info(f"Documento criado com sucesso.")
        return jsonify(new_document.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar o documento: {e}")
        return jsonify({'error': str(e)}), 400

# READ (GET) - Obter todos os documentos
@document_bp.route('/', methods=['GET'])
def get_all_documents():
    documents = Document.query.all()
    return jsonify([document.to_dict() for document in documents]), 200

# READ (GET) - Obter um documento específico pelo ID
@document_bp.route('/<int:id>', methods=['GET'])
def get_document(id):
    document = Document.query.get_or_404(id)
    return jsonify(document.to_dict()), 200

# UPDATE (PUT) - Atualizar um documento pelo ID
@document_bp.route('/<int:id>', methods=['PUT'])
def update_document(id):
    document = Document.query.get_or_404(id)
    data = request.get_json()

    try:
        # Atualizar apenas os campos que foram enviados
        document.file = data.get('file', document.file)
        document.description = data.get('description', document.description)
        document.stage = data.get('stage', document.stage)
        document.related_stage = data.get('related_stage', document.related_stage)
        document.name = data.get('name', document.name)
        document.temporal = data.get('temporal', document.temporal)
        document.document_type = data.get('document_type', document.document_type)

        # Commit para salvar as mudanças no banco de dados
        db.session.commit()

        return jsonify(document.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar o documento: {e}")
        return jsonify({'error': str(e)}), 400

# DELETE (DELETE) - Deletar um documento pelo ID
@document_bp.route('/<int:id>', methods=['DELETE'])
def delete_document(id):
    document = Document.query.get_or_404(id)

    try:
        db.session.delete(document)
        db.session.commit()
        logging.info(f"Documento deletado com sucesso.")
        return jsonify({'message': 'Documento deletado com sucesso.'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar o documento: {e}")
        return jsonify({'error': str(e)}), 400
