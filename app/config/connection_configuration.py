import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

load_dotenv()
server_name = os.getenv("SERVER_NAME")
database_name = os.getenv("DATABASE_NAME")
username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
database_url = os.getenv("DATABASE_URL")

connection_url = database_url
engine = create_engine(connection_url, echo=True)

metadata = MetaData()

metadata.bind = engine

Session = sessionmaker(bind=engine)

try:
    session = Session()
    result = session.execute(text("SELECT DB_NAME()")).scalar()
    print("Connected to database:", result)

except Exception as e:
    print("Error connecting to the database:", e)

finally:
    session.close()
