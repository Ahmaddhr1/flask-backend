from flask import Flask
from config.db import db, test_db_connection
from config import db as db_config
from models import Complex, Admin, Building
from routes.auth import auth

app = Flask(__name__)

app.config.from_object(db_config)

db.init_app(app)

test_db_connection(app)

app.register_blueprint(auth)

@app.route('/')
def home():
    return "App is runningg!"

if __name__ == '__main__':
    app.run(debug=True)