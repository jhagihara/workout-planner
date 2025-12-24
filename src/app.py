from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
import os
from db import db
from models import User

# my notes:
# 1. uses SQLAlchemy because it's an object relational mapper that can convert data from db -> python

def create_app():
    app = Flask(__name__)
    url = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    # added migrations for when I decide to expand the db
    # connects flask, the db and Alembic
    Migrate(app, db)

    # '/test-db' calls the function to test the connection to the database
    @app.route('/test-db')
    def test_db():
        try:
            # have to wrap it in text()
            db.session.execute(text("SELECT 1;"))
            return "Database Connection Success"
        except Exception as e:
            return f"Database Connection Fail: {e}"

    # home page
    @app.route("/")
    def home():
        users = User.query.all()
        return jsonify([{"id": u.id, "name": u.name} for u in users])
        #return "hello"


    return app

app = create_app()

