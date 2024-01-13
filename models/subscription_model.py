from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, ForeignKey
from config.connection_configuration import engine

meta = MetaData(bind=engine)       
         
subscription_table = Table(
    "dbo.tblSubscription",
    meta,
    Column("idSubscription", Integer, primary_key=True),
    Column("dtPayment", String),
    Column("dtDateOfSignUp", Date),
    Column("dt7DaysFree", Integer),
    Column("dtInviteDiscountStatus", Boolean),
    Column("dtSubscriptionPrice", float),
    Column("fiType", Integer, ForeignKey("quality.idType")),
)

