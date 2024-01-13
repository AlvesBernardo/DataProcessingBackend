from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, Interval ,ForeignKey , func
from config.connection_configuration import engine
from enum import Enum

meta = MetaData(bind=engine)
db_tblAccount = Table(
        "dbo.tblAccounts",
        meta,
    Column("idAccounnt",Integer, primary_key=True),
    Column("dtEmail",String(250), unique=True, nullable=False),
    Column("dtPassword",String(250), nullable=False),
    Column("dtIsAccountBlocked", Boolean,  default=False),
    Column("dtIsAdmin", Boolean, default=False),
    Column("dtLanguage", String(50)),
    Column("isAccountActivated",Boolean, deafult=False),
    Column("fiSubscription".Integer, ForeignKey("tblSubscription.idSubscription")),

)