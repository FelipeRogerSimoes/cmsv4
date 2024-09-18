import os
from openpyxl import Workbook
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import db, Person, InsuranceCompany, Broker, Case, Operations, SystemUser, Routine, Task, Event, Parameter, \
    Validation, Field, Action, Timesheet, Expense, Policy, Document
from config import Config  # Importa a configuração do caminho do banco de dados

# Usar o caminho do banco de dados definido no Config
DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI

# Criar engine e sessão do SQLAlchemy
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


# Função para exportar uma tabela específica para um arquivo Excel
def export_table_to_xlsx(model, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = model.__tablename__

    # Obter os nomes das colunas da tabela
    inspector = inspect(engine)
    columns = [column['name'] for column in inspector.get_columns(model.__tablename__)]

    # Adicionar os cabeçalhos no Excel
    ws.append(columns)

    # Adicionar os dados das linhas
    rows = session.query(model).all()
    for row in rows:
        ws.append([getattr(row, column) for column in columns])

    # Salvar o arquivo Excel
    output_dir = os.path.join(Config.BASE_DIR, 'exports')  # Usar BASE_DIR do Config
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)
    wb.save(filepath)
    return filepath


# Função para exportar todas as tabelas
def export_all_tables_to_xlsx():
    models = [Person, InsuranceCompany, Broker, Case, Operations, SystemUser, Routine, Task, Event, Parameter,
              Validation, Field, Action, Timesheet, Expense, Policy, Document]

    for model in models:
        filename = f'{model.__tablename__}.xlsx'
        filepath = export_table_to_xlsx(model, filename)
        print(f"Exported {model.__tablename__} to {filepath}")


if __name__ == '__main__':
    export_all_tables_to_xlsx()
