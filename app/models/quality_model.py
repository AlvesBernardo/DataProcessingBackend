from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Quality(db.Model) : 
    __tablename__ = 'tblQuality'  # Specify the table name
    idType = db.Column(db.Integer, primary_key=True, nullable=False)  # PK INT NOT NULL
    dtDescription = db.Column(db.String(50), nullable=False)  # VAR(50) NOT NULL
    dtPrice = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Quality %r>' % self.idType