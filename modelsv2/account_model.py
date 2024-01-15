from flask import Flask
from config.connection_configuration import engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuring the engine in the Flask app
engine = create_engine('your_database_uri_here')

# Creating the SQLAlchemy instance
db = SQLAlchemy(app)
db.metadata.bind = engine

class Account(db.Model):
    idAccount = db.Column(db.Integer, primary_key=True)
    dtEmail = db.Column(db.String(50), nullable=False)
    dtPassword = db.Column(db.String(50), nullable=False)
    dtIsAccountBlocked = db.Column(db.Boolean(True), nullable=False, default=False)
    dtIsAdmin = db.Column(db.Boolean(True), nullable=False, default=False)
    fiSubscription = db.relationship("dbo.tbl0Subscription", backref="dbo.tblAccount")