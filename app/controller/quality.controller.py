from flask import Blueprint, jsonify
from sqlalchemy.orm import sessionmaker
from app.config.connection_configuration import engine, quality_table

quality_controller = Blueprint('quality', __name__)


@quality_controller.route('/quality', methods=['GET'])
def get_all_quality_types():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(quality_table).all()
    session.close()
    return jsonify(result)
