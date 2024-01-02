# app.py
from flask import Flask
from user_routes import user_routes
import sys

sys.path.append("..") # added!
from src.instances import quality_instances

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html', subscriptions=quality_instances)

@app.route('/select_subscription', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)
