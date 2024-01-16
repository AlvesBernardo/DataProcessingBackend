from flask import Flask
from config.connection_configuration import engine
from models.subtitle_model import Subtitle, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engine.url  # Use the configured database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/quality')
def test_connection():
    try:
        # Query the first row from the Quality table
        first_row = Subtitle.query.first()
        
        if first_row:
            result = f"First row: {first_row.idSubtitle}, {first_row.fiMovie}"
        else:
            result = "No records found in dbo.tblQuality"

        return result

    except Exception as e:
        return f"Error: {e}"



if __name__ == '__main__':
    app.run()
