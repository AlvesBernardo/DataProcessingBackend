from app.extensions import db


class Language(db.Model):
    __tablename__ = 'tblLanguage'
    idLanguage = db.Column(db.Integer, primary_key=True)
    dtDescription = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Quality %r>' % self.idLanguage
