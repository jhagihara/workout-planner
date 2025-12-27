from flask import Flask, jsonify, request
from sqlalchemy import text
from flask_migrate import Migrate
import os
from db import db
from models import User, Session, Workout

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

    # POST for adding a session for a specific user
    @app.route("/sessions", methods=["POST"])
    def create_session():
        data = request.get_json()

        # getting the user first
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"message": "User not found"}), 404


        session_type = data.get("session_type")
        muscle_group = data.get("muscle_group")
        duration_mins = data.get("duration_mins")

        new_session = Session(
            user=user,
            session_type=session_type,
            muscle_group=muscle_group,
            duration_mins=duration_mins
        )

        try:
            db.session.add(new_session)
            db.session.commit()
            return jsonify({
                "session_id": new_session.session_id,
                "user_id": new_session.user_id,
                "session_type": new_session.session_type,
                "muscle_group": new_session.muscle_group,
                "duration_mins": new_session.duration_mins
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error creating session: {e}"}), 500


    # GET for retrieving all sessions for all users
    @app.route("/sessions", methods=["GET"])
    def get_sessions():
        sessions = Session.query.all()

        result = []
        for s in sessions:
            result.append({
                "session_id": s.session_id,
                "user_id": s.user_id,
                "session_type": s.session_type,
                "muscle_group": s.muscle_group,
                "duration_mins": s.duration_mins
            })
        return jsonify(result)

    # GET for getting all sessions from a specific user
    @app.route("/users/<int:user_id>/sessions", methods=["GET"])
    def get_user_sessions(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # filter session by the user
        # sessions = Session.query.filter_by(user=user).all()
        # or can do:
        sessions = user.sessions
        result = []
        for s in sessions:
            result.append({
                "session_id": s.session_id,
                "user_id": s.user_id,
                "session_type": s.session_type,
                "muscle_group": s.muscle_group,
                "duration_mins": s.duration_mins
            })
        return jsonify(result)

    # POST for creating a workout for a specific session
    @app.route("/workouts", methods=["POST"])
    def create_workout():
        data = request.get_json()

        # getting the user and session first
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"message": "User not found"}), 404
        session = Session.query.get(data['session_id'])
        if not session:
            return jsonify({"message": "Session not found"}), 404
        if session.user_id != user.user_id:
            return jsonify({"message": "Session does not belong to user"}), 400

        exercise_name = data.get("exercise_name")
        num_sets = data.get("num_sets")
        num_reps = data.get("num_reps")
        weight_lbs = data.get("weight_lbs")
        muscle = data.get("muscle")

        new_workout = Workout(
            user=user,
            session=session,
            exercise_name=exercise_name,
            num_sets=num_sets,
            num_reps=num_reps,
            weight_lbs=weight_lbs,
            muscle=muscle
        )

        try:
            db.session.add(new_workout)
            db.session.commit()
            return jsonify({
                "workout_id": new_workout.workout_id,
                "session_id": new_workout.session_id,
                "user_id": new_workout.user_id,
                "exercise_name": new_workout.exercise_name,
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error creating workout: {e}"}), 500

    # GET for retrieving all workouts
    @app.route("/workouts", methods=["GET"])
    def get_workouts():
        workouts = Workout.query.all()

        result = []
        for w in workouts:
            result.append({
                "workout_id": w.workout_id,
                "session_id": w.session_id,
                "user_id": w.user_id,
                "exercise_name": w.exercise_name,
                "num_sets": w.num_sets,
                "num_reps": w.num_reps,
                "weight_lbs": str(w.weight_lbs),
                "muscle": w.muscle
            })

        return jsonify(result)


    # GET for retrieving all workouts for a session
    @app.route("/sessions/<int:session_id>/workouts", methods=["GET"])
    def get_session_workouts(session_id):
        session = Session.query.get(session_id)
        if not session:
            return jsonify({"message": "Session not found"}), 404

        # retrieve all workouts for that session
        workouts = session.workouts
        result = []
        for w in workouts:
            result.append({
                "workout_id": w.workout_id,
                "session_id": w.session_id,
                "user_id": w.user_id,
                "exercise_name": w.exercise_name,
                "num_sets": w.num_sets,
                "num_reps": w.num_reps,
                "weight_lbs": str(w.weight_lbs),
                "muscle": w.muscle
            })

        return jsonify(result)

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
        return "hello"


    return app

app = create_app()

