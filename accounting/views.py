# You will probably need more methods from flask but this one is a good start.
from flask import render_template

# Import things from Flask that we need.
from accounting import app, db

# Import our models
from models import Contact, Invoice, Policy

# Routing for the server.
@app.route("/")
def index():
    # An example of accessing a card by name and returning the first result.
    # card = db.session.query(Card).filter(Card.name == 'Naturalize').first()

    # You will need to serve something up here.
    return render_template('index.html')
