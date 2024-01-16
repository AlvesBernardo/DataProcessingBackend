from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from your_database_module import engine, quality_table
account_controller = Blueprint('quality', __name__)

##Only allow select queries while using orm
@account_controller.route('/account', methods=['GET'])
def get_account():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(quality_table).all()
    session.close()
    return jsonify(result)