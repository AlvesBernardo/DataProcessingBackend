from flask import Flask
from .config.connection_configuration import engine
from .services.emailSender import send_email
from .extensions import db
from .models.view_model import View

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engine.url  # Use the configured database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



@app.route('/email')
def sendingEmail():  # put application's code here
     send_email('mahdisadeghi.business@gmail.com')

@app.route('/quality')
def test_connection():
    try:

        # Query the first row from the Quality table
        first_row = View.query.first()
        
        if first_row:
            result = f"First row: {first_row.idView}"
        else:
            result = "No records found in dbo.tblQuality"

        return result

    except Exception as e:
        return f"Error: {e}"



if __name__ == '__main__':
    app.run()
