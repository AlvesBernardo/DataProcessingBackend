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

# SQL Server connection URL
connection_url = "mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server"

# Create SQLAlchemy engine
engine = create_engine(connection_url, echo=True)  # Set echo to True for debugging

# Create a MetaData object
metadata = MetaData()

# Bind the engine to the MetaData
metadata.bind = engine

# Now you can use the 'engine' and 'metadata' objects to interact with the database
# For example, you can use metadata to reflect the database schema:
# metadata.reflect()

# Or you can create a connection to the database
# connection = engine.connect()

# Don't forget to close the connection when you're done
# connection.close()

Session = sessionmaker(bind=engine)
try:
    # Create a session
    session = Session()

    # Execute a simple query (e.g., selecting the current database name)
    result = session.execute(text("SELECT DB_NAME()")).scalar()
    print("Connected to database:", result)

except Exception as e:
    print("Error connecting to the database:", e)

finally:
    # Close the session
    session.close()