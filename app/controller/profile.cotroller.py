from flask import Blueprint, jsonify
from sqlalchemy.orm import sessionmaker
from app.config.connection_configuration import engine, quality_table

profile_controller = Blueprint('quality', __name__)


@profile_controller.route('/quality', methods=['GET'])
def profille_contoller():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(quality_table).all()
    session.close()
    return jsonify(result)
