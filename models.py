from flask_sqlalchemy import SQLAlchemy

# Instância global do SQLAlchemy
db = SQLAlchemy()

# Modelo para a tabela 'Person'
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

# Modelo para a tabela 'Cases'
class Cases(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    insurance_company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
    # Definição de outros campos conforme necessário

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'entry_date': self.entry_date.isoformat(),
            'status': self.status,
            'insurance_company_id': self.insurance_company_id
        }

# Exemplo de outro modelo: InsuranceCompany
class InsuranceCompany(db.Model):
    __tablename__ = 'insurance_company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))  # Relacionamento com a tabela 'person'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'person_id': self.person_id
        }

# Outros modelos conforme a necessidade (Broker, SystemUser, Timesheets, etc.)

