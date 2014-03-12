#!/user/bin/env python2.7

from datetime import datetime

from accounting import db
from models import Contact, Invoice, Policy

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
        self.date_cursor = datetime.now().date()
        self.policy = db.Policy.query.filter_by(id=policy_id).one()

        #This is a new policy, make the invoices
        if not db.Invoice.query.filter_by(policy_id=policy_id):
            self.make_invoices_for_policy()

    def return_account_balance(self, date_cursor):
        pass

    def make_payment(self, date_cursor):
        pass

    def cancel_policy(self):
        pass

    def return_all_invoices(self):
        pass

    def make_invoices_for_policy(self):
        pass

