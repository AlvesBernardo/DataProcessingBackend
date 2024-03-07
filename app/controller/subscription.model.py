from flask import Blueprint, jsonify
from sqlalchemy.orm import sessionmaker
from app.config.connection_configuration import engine, subscription_table

subscription_controller = Blueprint('subscription', __name__)


@subscription_controller.route('/subscription/<int:user_id>', methods=['GET'])
def get_subscription(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(subscription_table).filter_by(user_id=user_id).first()
    session.close()
    return jsonify(result)
