from flask import Flask
from app.services.emailSender import send_email

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    send_email('mahdisadeghi.business@gmail.com')


if __name__ == '__main__':
    app.run()
