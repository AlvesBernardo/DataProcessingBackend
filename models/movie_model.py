from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, ForeignKey , Date , Interval
from config.connection_configuration import engine
from datetime import timedelta
meta = MetaData(bind=engine)
view_table = Table(
    "movie",
    meta,
    Column("idMovie", Integer, primary_key=True),
    Column("dtTitle", String),
    Column("dtYear", Date),
    Column("dtAmountOfEp", Integer),
    Column("dtAmountOfSeasons", Integer),
    Column("dtLength", Interval , server_default=timedelta(seconds=0)),
    Column("dtMinAge", Integer),
    Column("fiType", Integer, ForeignKey("type.idType")),
    Column("fiGenre", Integer, ForeignKey("genre.idGenre")),
    Column("fiLanguage", Integer, ForeignKey("language.idLanguage"))
)