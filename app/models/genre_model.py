from app.extensions import db


class Genre(db.Model):
    __tablename__ = 'tblGenre'
    idGenre = db.Column(db.Integer, primary_key=True)
    dtDescription = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Genre %r>' % self.idGenre
