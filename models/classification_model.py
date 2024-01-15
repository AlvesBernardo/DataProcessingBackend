from sqlalchemy import Table, Column, Integer, String, MetaData
from config.connection_configuration import engine

try:
    # Attempt to create a connection to the database
    meta = MetaData()
    meta.bind = engine


    view_table = Table(
        "classification",
        meta,
        Column("idClassification", Integer, primary_key=True),
        Column("dtDescription", String)
    )

    # Perform any additional operations using the view_table or meta if needed

    print("Connection to the database successful!")

except Exception as e:
    print(f"An error occurred: {e}")
