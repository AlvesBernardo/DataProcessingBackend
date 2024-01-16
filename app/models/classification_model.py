
from sqlalchemy import Table, Column, Integer, String, MetaData
from app.config.connection_configuration import engine
from app.extensions import db
meta = MetaData()
meta.bind = engine
db.init_app(meta)
class Classification(db.Model):
    idClassification = db.Column(db.Integer, primary_key=True)
    dtDescription = db.Column(db.String(50), nullable=False)
    