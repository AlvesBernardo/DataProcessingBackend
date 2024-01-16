import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import text

load_dotenv()
server_name = "dataprocessing-sbmr.database.windows.net"
database_name = "dataprocessing-sbmr"
username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")

# SQL Server connection URL formatting
connection_url = f"mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server"

# Create SQLAlchemy engine
engine = create_engine(connection_url, echo=True)  # Set echo to True for debugging

# Create a MetaData object
metadata = MetaData()

# Bind the engine to the MetaData
metadata.bind = engine

Session = sessionmaker(bind=engine)

try:
    # Create a session instance
    session = Session()

    # Execute a simple query (e.g., selecting the current database name)
    result = session.execute(text("SELECT DB_NAME()")).scalar()
    print("Connected to database:", result)

except Exception as e:
    print("Error connecting to the database:", e)

finally:
    # Close the session
    session.close()
