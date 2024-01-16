from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from app.config.connection_configuration import engine, quality_table

profille_contoller = Blueprint('quality', __name__)

##Only allow select queries while using orm
@profille_contoller.route('/quality', methods=['GET'])
def profille_contoller():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(quality_table).all()
    session.close()
    return jsonify(result)