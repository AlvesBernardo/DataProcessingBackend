from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from your_database_module import engine, quality_table

quality_controller = Blueprint('quality', __name__)

##Only allow select queries while using orm
@quality_controller.route('/quality', methods=['GET'])
def get_all_quality_types():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(quality_table).all()
    session.close()
    return jsonify(result)