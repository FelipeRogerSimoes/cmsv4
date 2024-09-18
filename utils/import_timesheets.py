import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from config import Config  # Importa a configuração do caminho do banco de dados

# Definir o caminho do banco de dados
DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI  # Certifique-se de que está correto

# Criar a engine e sessão do SQLAlchemy
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Definir o modelo da tabela 'timesheet'
Base = declarative_base()

class Timesheet(Base):
    __tablename__ = 'timesheet'

    id = Column(Integer, primary_key=True)
    case_id = Column(Integer)
    billing_type = Column(String)
    activity_type = Column(String)
    lead_adjuster = Column(Integer)
    approved_by_manager = Column(Boolean)
    approved_by_director = Column(Boolean)
    billed = Column(Boolean)
    invoice = Column(String)
    description = Column(String)
    activity_date = Column(Date)
    hours_worked = Column(Float)
    rate = Column(Float)
    fee = Column(Float)
    excluded = Column(Boolean)

# Função para converter valores de string ou Excel para booleano
def parse_boolean(value):
    return value == 'TRUE' or value is True

# Função revisada para converter valores de string ou Excel para datas
def parse_date(value):
    if pd.isnull(value):  # Verificar se o valor é nulo
        return None
    if isinstance(value, datetime):  # Verificar se já é uma instância datetime
        return value
    try:
        return datetime.strptime(str(value), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        print(f"Erro ao converter data: {value}")
        return None

# Função para carregar os dados do arquivo Excel e inserir no banco
def insert_timesheets_from_excel(file_path):
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(file_path)

        # Verificar se os dados foram lidos corretamente
        print(f"Linhas carregadas do Excel: {len(df)}")

        # Processar os dados
        for index, row in df.iterrows():
            timesheet = Timesheet(
                id=row['id'],
                case_id=row['case_id'],
                billing_type=row['billing_type'],
                activity_type=row['activity_type'],
                lead_adjuster=row['lead_adjuster'],
                approved_by_manager=parse_boolean(row['approved_by_manager']),
                approved_by_director=parse_boolean(row['approved_by_director']),
                billed=parse_boolean(row['billed']),
                invoice=row['invoice'],
                description=row['description'],
                activity_date=parse_date(row['activity_date']),
                hours_worked=row['hours_worked'],
                rate=row['rate'],
                fee=row['fee'],
                excluded=parse_boolean(row['excluded'])
            )

            # Adicionar à sessão
            try:
                session.add(timesheet)
                session.commit()  # Confirma as mudanças no banco
                print(f"Linha {row['id']} inserida com sucesso.")
            except IntegrityError as e:
                session.rollback()  # Reverter em caso de erro
                print(f"Erro de integridade ao inserir ID {row['id']}: {e}")
            except Exception as e:
                session.rollback()
                print(f"Erro ao inserir ID {row['id']}: {e}")

    except Exception as e:
        print(f"Erro ao processar o arquivo Excel: {e}")

# Executar a função com o caminho para o arquivo Excel
if __name__ == '__main__':
    file_path = 'timesheet.xlsx'  # Defina o caminho do seu arquivo Excel
    insert_timesheets_from_excel(file_path)
