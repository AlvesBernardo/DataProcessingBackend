from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, ForeignKey
from config.connection_configuration import engine

meta = MetaData(bind=engine)

quality_table = Table(
    "quality",
    meta,
    Column("idType", Integer, primary_key=True),
    Column("dtDescription", String),
    Column("dtPrice", float),
)