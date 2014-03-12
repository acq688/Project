#!/user/bin/env python2.7

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from accounting import db
from models import Contact, Invoice, Payment, Policy

"""
#######################################################
This is the base code for the intern project.

If you have any questions, please contact Amanda at:
    watchmen@britecore.com
#######################################################
"""

class PolicyAccounting(object):
    """
     Each policy has its own instance of accounting.
    """
    def __init__(self, policy_id):
        self.policy = Policy.query.filter_by(id=policy_id).one()

        if not self.policy.invoices:
            #Make some invoices so I stop forgetting
            self.make_invoices()

    def return_account_balance(self, date_cursor=None):
        if not date_cursor:
            date_cursor = datetime.now().date()

        #Put in a problem with date here for a unit test
        invoices = Invoice.query.filter_by(policy_id=self.policy.id)\
                                .filter(Invoice.bill_date <= date_cursor)\
                                .order_by(Invoice.bill_date)\
                                .all()
        due_now = 0
        for invoice in invoices:
            due_now += invoice.amount_due

        payments = Payment.query.filter_by(policy_id=self.policy.id)\
                                .filter(Payment.transaction_date <= date_cursor)\
                                .all()
        for payment in payments:
            due_now -= payment.amount_paid

        return due_now

    def make_payment(self, date_cursor=None, amount=0):
        if not date_cursor:
            date_cursor = datetime.now().date()

        payment = Payment(self.policy.id,
                          amount,
                          date_cursor)
        db.session.add(payment)
        db.session.commit()

    def evaluate_cancel(self, date_cursor=None):
        if not date_cursor:
            date_cursor = datetime.now().date()

        invoices = Invoice.query.filter_by(policy_id=self.policy.id)\
                                .filter(Invoice.cancel_date <= date_cursor)\
                                .order_by(Invoice.bill_date)\
                                .all()

        for invoice in invoices:
            if not self.return_account_balance(invoice.cancel_date):
                continue
            else:
                print "THIS POLICY SHOULD HAVE CANCELED"
                break
        else:
            print "THIS POLICY SHOULD NOT CANCEL"


    def make_invoices(self):
        """
         This creates the invoices for whichever policy
         this PolicyAccounting instance is looking at.
         If invoices currently exist, it deletes them.
        """
        for invoice in self.policy.invoices:
            invoice.delete()

        invoices = []
        first_invoice = Invoice(self.policy.id,
                                self.policy.effective_date, #bill_date
                                self.policy.effective_date + relativedelta(months=1), #due
                                self.policy.effective_date + relativedelta(months=1, days=14), #cancel
                                self.policy.annual_premium)
        invoices.append(first_invoice)

        if self.policy.billing_schedule == "Annual":
            pass
        elif self.policy.billing_schedule == "Quarterly":
            first_invoice.amount_due = first_invoice.amount_due * 0.25
            for i in range(1, 4):
                months_after_eff_date = i*3
                due_date = self.policy.effective_date + relativedelta(months=months_after_eff_date)
                invoice = Invoice(self.policy.id,
                                  due_date,
                                  due_date + relativedelta(months=1),
                                  due_date + relativedelta(months=1, days=14),
                                  self.policy.annual_premium * 0.25)
                invoices.append(invoice)
        elif self.policy.billing_schedule == "Monthly":
            #Maybe make them implement monthly?
            pass
        else:
            print "You have chosen a bad billing schedule."

        for invoice in invoices:
            db.session.add(invoice)
        db.session.commit()

#Need to put this into an initial.sql
def insert_data():
    #Contacts
    contacts = []
    john_doe_agent = Contact('John Doe', 'Agent')
    contacts.append(john_doe_agent)
    john_doe_insured = Contact('John Doe', 'Named Insured')
    contacts.append(john_doe_insured)
    bob_smith = Contact('Bob Smith', 'Agent')
    contacts.append(bob_smith)
    anna_white = Contact('Anna White', 'Named Insured')
    contacts.append(anna_white)
    joe_lee = Contact('Joe Lee', 'Agent')
    contacts.append(joe_lee)
    ryan_bucket = Contact('Ryan Bucket', 'Named Insured')
    contacts.append(ryan_bucket)

    for contact in contacts:
        db.session.add(contact)
    db.session.commit()

    policies = []
    p1 = Policy('Policy One', date(2015, 1, 1), 365)
    p1.billing_schedule = 'Annual'
    p1.named_insured = john_doe_insured.id
    p1.agent = bob_smith.id
    policies.append(p1)

    p2 = Policy('Policy Two', date(2015, 2, 1), 1600)
    p2.billing_schedule = 'Quarterly'
    p2.named_insured = anna_white.id
    p2.agent = joe_lee.id
    policies.append(p2)

    p3 = Policy('Policy Three', date(2015, 1, 1), 1200)
    p3.billing_schedule = 'Monthly'
    p3.named_insured = ryan_bucket.id
    p3.agent = john_doe_agent.id
    policies.append(p3)

    for policy in policies:
        db.session.add(policy)
    db.session.commit()

    payment_for_p2 = Payment(p2.id, 400, date(2015, 2, 1))
    db.session.add(payment_for_p2)
    db.session.commit()

