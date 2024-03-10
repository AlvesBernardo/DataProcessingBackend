from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import logging
from datetime import date, time

db = SQLAlchemy()
logger = logging.getLogger(__name__)


def serialize_date(d):
    if isinstance(d, date):
        return d.strftime('%Y-%m-%d')
    return None


def serialize_time(t):
    if isinstance(t, time):
        return t.strftime('%H:%M:%S')
    return None


def call_stored_procedure_get(procedure_name: str, params: dict = None):
    connection = db.engine.raw_connection()
    try:
        cursor = connection.cursor()
        procedure_name = f"EXEC dbo.{procedure_name}"
        stored_procedure = text(procedure_name)
        if params is None:
            cursor.execute(procedure_name)
        else:
            cursor.execute(stored_procedure, **params)
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        serialized_results = []
        for row in results:
            serialized_row = {}
            for column, value in zip(columns, row):
                if isinstance(value, date):
                    serialized_row[column] = serialize_date(value)
                elif isinstance(value, time):
                    serialized_row[column] = serialize_time(value)
                else:
                    serialized_row[column] = value
            serialized_results.append(serialized_row)
        return serialized_results
    finally:
        cursor.close()
        connection.close()


def call_stored_procedure_post(procedure_name: str, param_value_list: tuple):
    connection = db.engine.raw_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(procedure_name, param_value_list)
        connection.commit()
        return cursor.messages
    except Exception as e:
        connection.rollback()
        
        return None

    finally:
        cursor.close()
        connection.close()
