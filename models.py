from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Tipo: 'physical' (pessoa física) ou 'legal' (empresa)
    cpf_cnpj = db.Column(db.String(20), unique=True, nullable=False)  # CPF ou CNPJ

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'cpf_cnpj': self.cpf_cnpj
        }

class Cases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    insurance_company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
    # Outros campos...

# Outras tabelas como InsuranceCompany, Broker, SystemUser, etc.
