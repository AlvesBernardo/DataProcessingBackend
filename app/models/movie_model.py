from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
from app.extensions import db


class Movie(db.Model) : 
    idMovie = db.Column(db.Integer, primary_key=True)
    dtTitle = db.Column(db.String)
    dtYear = db.Column(db.Date)
    dtAmountOfEp = db.Column(db.Integer)
    dtAmountOfSeasons = db.Column(db.Integer)
    dtLength = db.Column(db.Interval)
    dtMinAge = db.Column(db.Integer)
    fiType = db.Column(db.Integer, db.ForeignKey("type.idType"))
    fiGenre = db.Column(db.Integer, db.ForeignKey("genre.idGenre"))
    fiLanguage = db.Column(db.Integer, db.ForeignKey("language.idLanguage"))
    