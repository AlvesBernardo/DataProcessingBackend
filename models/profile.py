from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, Interval ,ForeignKey , func
from config.connection_configuration import engine
from enum import Enum

meta = MetaData(bind=engine)
db_tblProfile = Table(
        "dbo.tblProfile",
        meta,
    Column("idUser",Integer, primary_key=True),
    Column("dtName",String(250), unique=True, nullable=False),
    Column("dtPicture",String(50), nullable=False),
    Column("dtIsMinor", Boolean,  default=False),
    Column("dtLanguage", String(50), default=False),
    Column("dtLanguage", String(50)),
    Column("fiAccount",Integer,  ForeignKey("dbo.tblAccount.idGenre")),
    Column("fiGenre",Integer, ForeignKey("tblGenre.idGenre")),
)

