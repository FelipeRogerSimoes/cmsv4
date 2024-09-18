from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo Person
class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(10))  # Tipo: 'physical' (pessoa física) ou 'legal' (empresa)
    cpf_cnpj = db.Column(db.String(20), unique=True, nullable=False)  # CPF ou CNPJ
    email = db.Column(db.String(255), nullable=True)  # Novo campo: email
    whatsapp = db.Column(db.String(20), nullable=True)  # Novo campo: whatsapp
    role = db.Column(db.String(255), nullable=True)  # Novo campo: role
    address = db.Column(db.Text, nullable=True)  # Novo campo: endereço
    deleted = db.Column(db.Boolean, default=False)  # Controle de exclusão lógica

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'cpf_cnpj': self.cpf_cnpj,
            'email': self.email,
            'whatsapp': self.whatsapp,
            'role': self.role,
            'address': self.address,
            'deleted': self.deleted
        }

# Modelo InsuranceCompany
class InsuranceCompany(db.Model):
    __tablename__ = 'insurance_company'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id
        }

# Modelo Broker
class Broker(db.Model):
    __tablename__ = 'broker'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    person = db.relationship('Person', backref=db.backref('broker', lazy=True))

# Modelo Case
class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    judicial_action = db.Column(db.Boolean, nullable=True)
    policy_number = db.Column(db.String(255), nullable=True)
    reported_to_insurer = db.Column(db.Boolean, nullable=True)
    case_name = db.Column(db.String(255), nullable=True)
    case_number = db.Column(db.String(255), nullable=True, unique=True)
    condition = db.Column(db.String(50), nullable=True)
    broker = db.Column(db.String(255), nullable=True)
    entry_date = db.Column(db.Date, nullable=True)
    loss_date = db.Column(db.Date, nullable=True)
    notification_date = db.Column(db.Date, nullable=True)
    fee_estimate = db.Column(db.Numeric(10, 2), nullable=True)
    damage_estimate = db.Column(db.Numeric(10, 2), nullable=True)
    salvage_estimate = db.Column(db.Numeric(10, 2), nullable=True)
    excluded = db.Column(db.Boolean, nullable=True)
    fee_limit = db.Column(db.Numeric(10, 2), nullable=True)
    incident_location = db.Column(db.Text, nullable=True)
    operation_id = db.Column(db.Integer, db.ForeignKey('operations.id'))
    rate_2 = db.Column(db.Boolean, nullable=True)
    insurer_reference = db.Column(db.String(255), nullable=True)
    lead_adjuster = db.Column(db.String(255), nullable=True)
    auxiliary_adjuster = db.Column(db.String(255), nullable=True)
    reserve = db.Column(db.Numeric(10, 2), nullable=True)
    salvage = db.Column(db.Boolean, nullable=True)
    search = db.Column(db.Text, nullable=True)
    insured_name = db.Column(db.String(255), nullable=True)
    insurer_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
    status = db.Column(db.String(50), nullable=True)
    temporal = db.Column(db.Boolean, nullable=True)
    billing_type = db.Column(db.String(50), nullable=True)
    fee_limit_value = db.Column(db.Numeric(10, 2), nullable=True)
    physical_inspection = db.Column(db.Boolean, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'judicial_action': self.judicial_action,
            'policy_number': self.policy_number,
            'reported_to_insurer': self.reported_to_insurer,
            'case_name': self.case_name,
            'case_number': self.case_number,
            'condition': self.condition,
            'broker': self.broker,
            'entry_date': self.entry_date,
            'loss_date': self.loss_date,
            'notification_date': self.notification_date,
            'fee_estimate': self.fee_estimate,
            'damage_estimate': self.damage_estimate,
            'salvage_estimate': self.salvage_estimate,
            'excluded': self.excluded,
            'fee_limit': self.fee_limit,
            'incident_location': self.incident_location,
            'operation_id': self.operation_id,
            'rate_2': self.rate_2,
            'insurer_reference': self.insurer_reference,
            'lead_adjuster': self.lead_adjuster,
            'auxiliary_adjuster': self.auxiliary_adjuster,
            'reserve': self.reserve,
            'salvage': self.salvage,
            'search': self.search,
            'insured_name': self.insured_name,
            'insurer_id': self.insurer_id,
            'status': self.status,
            'temporal': self.temporal,
            'billing_type': self.billing_type,
            'fee_limit_value': self.fee_limit_value,
            'physical_inspection': self.physical_inspection
        }


# Modelo Operations
class Operations(db.Model):
    __tablename__ = 'operations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    responsible = db.Column(db.Integer, db.ForeignKey('system_user.id'))
    group_name = db.Column(db.String(255), nullable=True)
    director = db.Column(db.Integer, db.ForeignKey('system_user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'responsible': self.responsible,
            'group_name': self.group_name,
            'director': self.director
        }

# Modelo SystemUser
class SystemUser(db.Model):
    __tablename__ = 'system_user'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    manager = db.Column(db.Integer, db.ForeignKey('system_user.id'), nullable=True)
    goal_type = db.Column(db.String(255), nullable=True)
    job_title = db.Column(db.String(255), nullable=True)
    level = db.Column(db.String(50), nullable=True)
    collaborator_type = db.Column(db.String(50), nullable=True)
    user_type = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'manager': self.manager,
            'goal_type': self.goal_type,
            'job_title': self.job_title,
            'level': self.level,
            'collaborator_type': self.collaborator_type,
            'user_type': self.user_type,
            'username': self.username,
            'active': self.active
        }

# Modelo Routine
# Modelo Routine
class Routine(db.Model):
    __tablename__ = 'routine'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    start_date = db.Column(db.Date, nullable=False)

    # Adicionar o método to_dict
    def to_dict(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'name': self.name,
            'status': self.status,
            'start_date': self.start_date.isoformat()  # Converter a data para string no formato ISO
        }

# Modelo Task
# Modelo Task
class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'), nullable=False)
    action = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    conclusion_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    mandatory = db.Column(db.Boolean, nullable=True)
    SLA = db.Column(db.Integer, nullable=True)
    responsible = db.Column(db.Integer, db.ForeignKey('system_user.id'))
    status = db.Column(db.String(50), nullable=True)
    condition = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'routine_id': self.routine_id,
            'action': self.action,
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'conclusion_date': self.conclusion_date.isoformat() if self.conclusion_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'document_id': self.document_id,
            'mandatory': self.mandatory,
            'SLA': self.SLA,
            'responsible': self.responsible,
            'status': self.status,
            'condition': self.condition
        }

# Modelo Event
class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=True)
    conditions = db.Column(db.Text, nullable=True)

# Modelo Parameter
class Parameter(db.Model):
    __tablename__ = 'parameter'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    operator = db.Column(db.String(10), nullable=True)
    validation_id = db.Column(db.Integer, db.ForeignKey('validation.id'))
    sequence = db.Column(db.Integer, nullable=True)

# Modelo Validation
class Validation(db.Model):
    __tablename__ = 'validation'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False)
    operator = db.Column(db.String(10), nullable=True)
    compared_value = db.Column(db.Numeric(10, 2), nullable=True)

# Modelo Field
class Field(db.Model):
    __tablename__ = 'field'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    sql_query = db.Column(db.Text, nullable=True)

# Modelo Action
class Action(db.Model):
    __tablename__ = 'action'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    function_name = db.Column(db.String(255), nullable=False)

# Modelo Timesheet
class Timesheet(db.Model):
    __tablename__ = 'timesheet'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    billing_type = db.Column(db.String(50), nullable=True)
    activity_type = db.Column(db.String(255), nullable=True)
    lead_adjuster = db.Column(db.String(255), nullable=True)
    approved_by_manager = db.Column(db.Boolean, nullable=True)
    approved_by_director = db.Column(db.Boolean, nullable=True)
    billed = db.Column(db.Boolean, nullable=True)
    invoice = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    activity_date = db.Column(db.Date, nullable=False)
    hours_worked = db.Column(db.Numeric(5, 2), nullable=True)
    rate = db.Column(db.Numeric(10, 2), nullable=True)
    fee = db.Column(db.Numeric(10, 2), nullable=True)
    excluded = db.Column(db.Boolean, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'billing_type': self.billing_type,
            'activity_type': self.activity_type,
            'lead_adjuster': self.lead_adjuster,
            'approved_by_manager': self.approved_by_manager,
            'approved_by_director': self.approved_by_director,
            'billed': self.billed,
            'invoice': self.invoice,
            'description': self.description,
            'activity_date': self.activity_date.strftime('%Y-%m-%d') if self.activity_date else None,
            'hours_worked': float(self.hours_worked) if self.hours_worked else None,
            'rate': float(self.rate) if self.rate else None,
            'fee': float(self.fee) if self.fee else None,
            'excluded': self.excluded
        }

# Modelo Expense
class Expense(db.Model):
    __tablename__ = 'expense'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    rate_limit = db.Column(db.Numeric(10, 2), nullable=True)
    declared_value = db.Column(db.Numeric(10, 2), nullable=True)
    expense_type = db.Column(db.String(50), nullable=True)
    expense_date = db.Column(db.Date, nullable=False)
    receipt_link = db.Column(db.Text, nullable=True)
    reimbursable = db.Column(db.Boolean, nullable=True)
    adjuster = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'rate_limit': self.rate_limit,
            'declared_value': self.declared_value,
            'expense_type': self.expense_type,
            'expense_date': self.expense_date,
            'receipt_link': self.receipt_link,
            'reimbursable': self.reimbursable,
            'adjuster': self.adjuster
        }

# Modelo Policy
class Policy(db.Model):
    __tablename__ = 'policy'

    id = db.Column(db.Integer, primary_key=True)
    affected_coverage = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)
    address_text = db.Column(db.String(255), nullable=True)
    excess = db.Column(db.Numeric(10, 2), nullable=True)
    hiring_method = db.Column(db.String(255), nullable=True)
    basic_excess = db.Column(db.Numeric(10, 2), nullable=True)
    franchise_lc = db.Column(db.Numeric(10, 2), nullable=True)
    policy_item = db.Column(db.String(255), nullable=True)
    policy_limit = db.Column(db.Numeric(10, 2), nullable=True)
    insured = db.Column(db.String(255), nullable=True)
    policy_number = db.Column(db.String(255), nullable=True)
    temporal = db.Column(db.Boolean, nullable=True)
    coverage_end_date = db.Column(db.Date, nullable=True)
    coverage_start_date = db.Column(db.Date, nullable=True)
    vrd_dm = db.Column(db.Numeric(10, 2), nullable=True)
    vrd_lc = db.Column(db.Numeric(10, 2), nullable=True)
    vrd_ppa = db.Column(db.Numeric(10, 2), nullable=True)

# Modelo Document
class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    stage = db.Column(db.String(255), nullable=True)
    related_stage = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    temporal = db.Column(db.Boolean, nullable=True)
    document_type = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'file': self.file,
            'description': self.description,
            'stage': self.stage,
            'related_stage': self.related_stage,
            'name': self.name,
            'temporal': self.temporal,
            'document_type': self.document_type
        }


class Rate(db.Model):
    __tablename__ = 'rate'

    id = db.Column(db.Integer, primary_key=True)
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameter.id'), nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(50), nullable=True)
    billing_type = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'parameter_id': self.parameter_id,
            'value': float(self.value),
            'type': self.type,
            'billing_type': self.billing_type
        }

# Tabela de metas de usuário
class UserGoal(db.Model):
    __tablename__ = 'user_goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('system_user.id'), nullable=False)
    goal_value = db.Column(db.Numeric(10, 2), nullable=False)  # Meta mensal total
    month = db.Column(db.Integer, nullable=False)  # Mês (1 a 12)
    year = db.Column(db.Integer, nullable=False)  # Ano da meta
    goal_hour = db.Column(db.Integer, nullable=False)  #Meta em horas
    user = db.relationship('SystemUser', backref='goals')

# Tabela de feriados
class Holiday(db.Model):
    __tablename__ = 'holidays'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)  # Data do feriado
    name = db.Column(db.String(255), nullable=True)  # Nome do feriado

# Tabela de atestados/férias
class UserLeave(db.Model):
    __tablename__ = 'user_leaves'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('system_user.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)  # Data de início
    end_date = db.Column(db.Date, nullable=False)  # Data de término
    leave_type = db.Column(db.String(50), nullable=False)  # Tipo de ausência ('Férias', 'Atestado')

    user = db.relationship('SystemUser', backref='leaves')