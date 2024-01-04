# app.py
from flask import Flask
import sys
sys.path.append("..") # added!
from src.instances import quality_instances
from services.auth_guard import auth_guard
app = Flask(__name__)
from flask import jsonify



@app.route('/')
def index():
    return render_template('index.html', subscriptions=quality_instances)

@app.route('/select_subscription', methods=['POST'])
@auth_guard()
def select_subscription():
    selected_subscription_index = int(request.form['subscription'])

    # onl allow selection of subscriptions from a list
    selected_subscription = quality_instances[selected_subscription_index]
    current_user.subscription = selected_subscription


    return f"Subscription {selected_subscription.get_description()} selected for the user!"

@app.route('/get_subscription', methods=['GET'])
def get_subscription(subscription):
    if current_user.subscription:
        subscription_info = {
            'description': current_user.subscription.get_description(),
            'price': current_user.subscription.get_price()
        }
        return f"User's Subscription: {subscription_info}"
    else:
        return "User has not selected a subscription yet."

# Dummy protected route
@app.route('/protected_route', methods=['GET'])
@auth_guard()
def protected_route():
    return "This is a protected route. You can only access it with a valid token."

if __name__ == '__main__':
    app.run(debug=True)
