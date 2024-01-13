from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Quality(db.Model) : 
    idQuality = db.Column(db.Integer, primary_key=True)
    dtQuality = db.Column(db.String)
    dtDescription = db.Column(db.String)
    
    def __repr__(self):
        return '<Quality %r>' % self.idQuality