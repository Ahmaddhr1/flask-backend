import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

load_dotenv()

db=SQLAlchemy()

SQLALCHEMY_DATABASE_URI =(
   f"mysql+mysqlconnector://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}" 
)

def test_db_connection(app):
    try:
        with app.app_context():
            # db.drop_all()
            db.session.execute(text("SELECT 1"))
            print("Database connected !")
            # db.create_all()
    except Exception as e:
        print("Error connecting to database",e)