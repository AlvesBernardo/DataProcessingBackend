from app.extensions import db
class Classification(db.Model):
    __tablename__ = 'tblClassification'
    idClassification = db.Column(db.Integer, primary_key=True)
    dtDescription = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return '<Quality %r>' % self.idClassification