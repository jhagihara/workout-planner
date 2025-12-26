from flask import Flask, jsonify, request
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

    # initialize the database with the app
    db.init_app(app)
    # added migrations for when I decide to expand the db
    # connects flask, the db and Alembic
    Migrate(app, db)

    # POST to create users
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        weight_lbs = data.get('weight_lbs')
        height_ft = data.get('height_ft')
        age = data.get('age')
        gender = data.get('gender')

        new_user = User(
            username=username,
            password=password,
            weight_lbs=weight_lbs,
            height_ft=height_ft,
            age=age,
            gender=gender)

        try:
            db.session.add(new_user)
            db.session.commit()

            # user successfully added - 201
            return jsonify({
                "user_id": new_user.user_id,
                "username": new_user.username
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error creating user: {e}"}), 500

    # GET to retrieve all users
    @app.route("/users", methods=["GET"])
    def get_users():
        users = User.query.all()

        result = []
        for u in users:
            result.append({
                "user_id": u.user_id,
                "username": u.username
            })

        return jsonify(result)

    # GET to get a single user by their user_id
    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify({
                "user_id": user.user_id,
                "username": user.username,
                "weight_lbs": str(user.weight_lbs),
                "height_ft": str(user.height_ft),
                "age": user.age,
                "gender": user.gender})

        # if the user isn't found
        return jsonify({"message": "User not found"}), 404

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
        #return jsonify([{"id": u.user_id, "name": u.username} for u in users])
        return "hello"


    return app

app = create_app()

