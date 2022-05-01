import os
from flask import Flask
from models import Document, db
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("USER_POSTGRES", "postgres")
user_password = os.getenv("PASSWORD_POSTGRES", "postgres")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{user_password}@localhost:5432/document"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def hello():
    db.create_all()
    doc = Document(2, 'hello')
    db.session.add(doc)
    db.session.commit()
    return {"hello": "world"}

if __name__ == '__main__':
    app.run(debug=True)