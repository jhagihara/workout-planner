from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# notes:
# 1. uses SQLAlchemy because it's an object relational mapper that can convert data from db -> python

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:your_password@localhost:5432/workout_planner"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# '/test-db' calls the function to test the connection to the database
@app.route('/test-db')
def test_db():
    try:
        db.session.execute("SELECT 1")
        return "Database Connection Success"
    except Exception as e:
        return f"Database Connection Fail: {e}"

    # confirming the server is running
@app.route("/")
def index():
    return "Server is running"

