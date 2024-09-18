import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from config import Config  # Importa a configuração do caminho do banco de dados

# Definir o caminho do banco de dados
DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI

# Criar a engine e sessão do SQLAlchemy
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Definir o modelo da tabela 'cases'
Base = declarative_base()

class Case(Base):
    __tablename__ = 'cases'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    judicial_action = Column(Boolean)
    policy_number = Column(Integer)
    reported_to_insurer = Column(Boolean)
    case_name = Column(String)
    case_number = Column(String)
    condition = Column(String)
    broker = Column(String)
    entry_date = Column(Date)
    loss_date = Column(Date)
    notification_date = Column(Date)
    fee_estimate = Column(Float)
    damage_estimate = Column(Float)
    salvage_estimate = Column(Float)
    excluded = Column(Boolean)
    fee_limit = Column(String)
    incident_location = Column(String)
    operation_id = Column(Integer)
    rate_2 = Column(Boolean)
    insurer_reference = Column(String)
    lead_adjuster = Column(Integer)
    auxiliary_adjuster = Column(Integer)
    reserve = Column(String)
    salvage = Column(String)
    search = Column(String)
    insured_name = Column(String)
    insurer_id = Column(Integer)
    status = Column(String)
    temporal = Column(String)
    billing_type = Column(String)
    fee_limit_value = Column(Float)
    physical_inspection = Column(Boolean)

# Função para converter valores de string ou Excel para booleano
def parse_boolean(value):
    return value == 'TRUE'

# Função revisada para converter valores de string ou Excel para datas
def parse_date(value):
    if pd.isnull(value):  # Verificar se o valor é nulo
        return None
    if isinstance(value, datetime):  # Verificar se já é uma instância datetime
        return value
    try:
        # Tentar converter strings para o formato de data (suporte a vários formatos)
        return datetime.strptime(value, '%Y-%m-%d')
    except (ValueError, TypeError):
        try:
            return pd.to_datetime(value).date()  # Caso seja um valor do Excel ou outro formato de data
        except:
            return None

# Função para carregar os dados do arquivo Excel e inserir no banco
def insert_cases_from_excel(file_path):
    # Ler o arquivo Excel
    df = pd.read_excel(file_path)

    # Processar os dados
    for index, row in df.iterrows():
        case = Case(
            id=row['id'],
            description=row['description'],
            judicial_action=parse_boolean(row['judicial_action']),
            policy_number=row['policy_number'],
            reported_to_insurer=parse_boolean(row['reported_to_insurer']),
            case_name=row['case_name'],
            case_number=row['case_number'],
            condition=row['condition'],
            broker=row['broker'],
            entry_date=parse_date(row['entry_date']),
            loss_date=parse_date(row['loss_date']),
            notification_date=parse_date(row['notification_date']),
            fee_estimate=row['fee_estimate'],
            damage_estimate=row['damage_estimate'],
            salvage_estimate=row['salvage_estimate'],
            excluded=parse_boolean(row['excluded']),
            fee_limit=row['fee_limit'],
            incident_location=row['incident_location'],
            operation_id=row['operation_id'],
            rate_2=parse_boolean(row['rate_2']),
            insurer_reference=row['insurer_reference'],
            lead_adjuster=row['lead_adjuster'],
            auxiliary_adjuster=row['auxiliary_adjuster'],
            reserve=row['reserve'],
            salvage=row['salvage'],
            search=row['search'],
            insured_name=row['insured_name'],
            insurer_id=row['insurer_id'],
            status=row['status'],
            temporal=row['temporal'],
            billing_type=row['billing_type'],
            fee_limit_value=row['fee_limit_value'],
            physical_inspection=parse_boolean(row['physical_inspection'])
        )

        # Tentar inserir o registro, ignorar duplicados
        try:
            session.add(case)
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Registro com ID {row['id']} já existe, ignorando...")

# Executar a função com o caminho para o arquivo Excel
if __name__ == '__main__':
    file_path = 'cases.xlsx'  # Defina o caminho do seu arquivo Excel
    insert_cases_from_excel(file_path)
