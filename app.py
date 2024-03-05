#  request: to make http requests, jsonify: to work with data in JSON format, make_response: to handle responses in python
from flask import Flask, request, jsonify, make_response

#  the ORM that helps us create tables and work with our DB
from flask_sqlalchemy import SQLAlchemy

#  a way to handle environment variables in python
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)

    def __init__(self, first_name, last_name, email, enrollment_date):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.enrollment_date = enrollment_date

    def json(self):
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "enrollment_date": (
                self.enrollment_date.isoformat() if self.enrollment_date else None
            ),
        }


#  to initialize the database
db.create_all()


#  creating a test route
@app.route("/test", methods=["GET"])
def test():
    return make_response(jsonify({"message": "test route"}), 200)


#  creating a student
@app.route("/students", methods=["POST"])
def add_student():
    try:
        #  getting the request
        data = request.get_json()
        #   createing the new student
        new_student = Student(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            enrollment_date=data["enrollment_date"],
        )
        #   creates the new student
        db.session.add(new_student)
        #   commit in the db
        db.session.commit()
        #   returning the okay response
        return make_response(jsonify({"message": "student created"}), 201)
    except Exception as e:
        return make_response(jsonify({"message": "error creating student"}), 500)


#  get all students
@app.route("/students", methods=["GET"])
def get_students():
    try:
        #  allows to query all existing students
        students = Student.query.all()
        return make_response(
            jsonify({"students": [student.json() for student in students]}), 200
        )
    except Exception as e:
        return make_response(jsonify({"message": "error getting students"}), 500)

#  update a student
@app.route("/students/<int:id>", methods=["PUT"])
def update_student_email(id):
    try:
        student = Student.query.filter_by(student_id=id).first()
        if student:
            data = request.get_json()
            student.email = data["email"]
            db.session.commit()
            return make_response(jsonify({"message": "student email updated"}), 200)
        return make_response(jsonify({"message": "student not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"message": "error updating student email"}), 500)


#  deleting a student
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    try:
        student = Student.query.filter_by(student_id=id).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return make_response(jsonify({"message": "user deleted"}), 200)

        return make_response(jsonify({"message": "student not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"message": "error deleting student"}), 500)
