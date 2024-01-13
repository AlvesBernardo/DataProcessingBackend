from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, Interval ,ForeignKey , func
from config.connection_configuration import engine
import datetime
meta = MetaData(bind=engine)
view_table = Table(
    "view",
    meta,
    Column("idView", Integer, primary_key=True),
    Column("dtMovieTime", Interval, nullable=False ),
    Column("fiSubtitle", Integer, ForeignKey("subtitle.idSubtitle")),
    Column("fiMovie", Integer, ForeignKey("movie.idMovie"))
)