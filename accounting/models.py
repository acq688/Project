from accounting import db
# from sqlalchemy.ext.declarative import declarative_base
# 
# DeclarativeBase = declarative_base()

class Policy(db.Model):
    __tablename__ = 'policies'

    __table_args__ = {}

    #column definitions
    id = db.Column(u'id', db.INTEGER(), primary_key=True, nullable=False)
    policy_number = db.Column(u'policy_number', db.VARCHAR(length=128), nullable=False)
    effective_date = db.Column(u'effective_date', db.DATE(), nullable=False)
    status = db.Column(u'status', db.Enum(u'Active', u'Canceled', u'Expired'), default=u'Active', nullable=False)
    billing_schedule = db.Column(u'billing_schedule', db.Enum(u'Annual', u'Quarterly', u'Monthly'), default=u'Annual', nullable=False)
    annual_premium = db.Column(u'annual_premium', db.INTEGER(), nullable=False)
    named_insured = db.Column(u'named_insured', db.INTEGER())
    agent = db.Column(u'agent', db.INTEGER())

    def __init__(self, policy_number, effective_date, annual_premium):
        self.policy_number = policy_number
        self.effective_date = effective_date
        self.annual_premium = annual_premium


class Contact(db.Model):
    __tablename__ = 'contacts'

    __table_args__ = {}

    #column definitions
    id = db.Column(u'id', db.INTEGER(), primary_key=True, nullable=False)
    name = db.Column(u'name', db.VARCHAR(length=128), nullable=False)
    role = db.Column(u'role', db.Enum(u'Named Insured', u'Agent'), nullable=False)

    def __init__(self, name, role):
        self.name = name
        self.role = role


class Invoice(db.Model):
    __tablename__ = 'invoices'

    __table_args__ = {}

    #column definitions
    id = db.Column(u'id', db.INTEGER(), primary_key=True, nullable=False)
    policy_id = db.Column(u'policy_id', db.INTEGER(), nullable=False)
    bill_date = db.Column(u'bill_date', db.DATE(), nullable=False)
    due_date = db.Column(u'due_date', db.DATE(), nullable=False)
    cancel_date = db.Column(u'cancel_date', db.DATE(), nullable=False)
    amount_due = db.Column(u'amount_due', db.INTEGER(), nullable=False)
    deleted = db.Column(u'deleted', db.Boolean, default=False, server_default='0', nullable=False)

    def __init__(self, policy_id, bill_date, due_date, cancel_date, amount_due):
        self.policy_id = policy_id
        self.bill_date = bill_date
        self.due_date = due_date
        self.cancel_date = cancel_date
        self.amount_due = amount_due
