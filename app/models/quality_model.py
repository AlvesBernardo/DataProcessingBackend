from app.extensions import db


class Quality(db.Model):
    __tablename__ = 'tblQuality'
    idType = db.Column(db.Integer, primary_key=True, nullable=False)
    dtDescription = db.Column(db.String(50), nullable=False)
    dtPrice = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Quality %r>' % self.idType
