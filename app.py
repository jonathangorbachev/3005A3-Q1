#  request: to make http requests, jsonify: to work with data in JSON format, make_response: to handle responses in python
from flask import Flask, request, jsonify, make_response

#  the ORM that helps us create tables and work with our DB
from flask_sqlalchemy import SQLAlchemy

#  a way to handle environment variables in python
from os import environ

# initializing new flask app
app = Flask(__name__)
# coonfiguring the SQLAlchemy database URI using an environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
# initializing SQLAlchemy with our flask app
db = SQLAlchemy(app)


# defining the student model
class Student(db.Model):
    # setting the name of the table
    __tablename__ = "students"

    # defining the columns for the students table
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)

    # the constructor in order to initialize the students table instance
    def __init__(self, first_name, last_name, email, enrollment_date):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.enrollment_date = enrollment_date

    # need this in order to convert students table to JSON, to use in HTTP requests
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
        #   returning all the students in our database with a 200 okay response status
        return make_response(
            jsonify({"students": [student.json() for student in students]}), 200
        )
    #  catching any errors
    except Exception as e:
        return make_response(jsonify({"message": "error getting students"}), 500)


#  update a student
@app.route("/students/<int:id>", methods=["PUT"])
def update_student_email(id):
    try:
        #   first finding a student with the given id, only need the first one hence "first()"
        student = Student.query.filter_by(student_id=id).first()
        #   if we do find a student in our database with this id, then update email
        if student:
            #  getting the body of the HTTP request
            data = request.get_json()
            #  setting the email of the found student with the email that was passed in through the body
            student.email = data["email"]
            #  comitting these new changes to our db
            db.session.commit()
            #  returning a 200 okay success response
            return make_response(jsonify({"message": "student email updated"}), 200)
        #   error message if the student wasn't found
        return make_response(jsonify({"message": "student not found"}), 404)
    except Exception as e:
        #  any error if an exception occurs
        return make_response(jsonify({"message": "error updating student email"}), 500)


#  deleting a student
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    try:
        student = Student.query.filter_by(student_id=id).first()
        if student:
            #   if we find a student with the given id, delete it from the database then commit our changes
            db.session.delete(student)
            db.session.commit()
            # return success response that the student was succesfully deleted
            return make_response(jsonify({"message": "student deleted"}), 200)
        # error messages for student not found and exception cases
        return make_response(jsonify({"message": "student not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"message": "error deleting student"}), 500)
