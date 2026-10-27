
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import mysql.connector
from mysql.connector import IntegrityError

app = Flask(__name__, template_folder=".", static_folder=None)
app.secret_key = "student_management_secret_key"


# Connect to MySQL database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="student_db"
    )


# Serve the CSS file
@app.route("/style.css")
def stylesheet():
    return send_from_directory(".", "style.css")


# Display all students
@app.route("/")
def index():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students ORDER BY id")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", students=students)


# Add a new student
@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    course = request.form.get("course", "").strip()
    semester = request.form.get("semester", "").strip()

    if not name or not email or not course or not semester:
        flash("Please fill in all fields.", "error")
        return redirect(url_for("index"))

    try:
        semester = int(semester)
        if not 1 <= semester <= 12:
            raise ValueError
    except ValueError:
        flash("Semester must be a number from 1 to 12.", "error")
        return redirect(url_for("index"))

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """INSERT INTO students (name, email, course, semester)
               VALUES (%s, %s, %s, %s)""",
            (name, email, course, semester)
        )
        connection.commit()
        flash("Student added successfully!", "success")

    except IntegrityError:
        connection.rollback()
        flash("That email address already exists.", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("index"))


# Edit an existing student
@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        course = request.form.get("course", "").strip()
        semester = request.form.get("semester", "").strip()

        if not name or not email or not course or not semester:
            flash("Please fill in all fields.", "error")
            cursor.close()
            connection.close()
            return redirect(url_for("edit_student", student_id=student_id))

        try:
            semester = int(semester)
            if not 1 <= semester <= 12:
                raise ValueError
        except ValueError:
            flash("Semester must be a number from 1 to 12.", "error")
            cursor.close()
            connection.close()
            return redirect(url_for("edit_student", student_id=student_id))

        try:
            cursor.execute(
                """UPDATE students
                   SET name = %s, email = %s, course = %s, semester = %s
                   WHERE id = %s""",
                (name, email, course, semester, student_id)
            )
            connection.commit()

            if cursor.rowcount == 0:
                flash("Student not found or no changes were made.", "error")
            else:
                flash("Student updated successfully!", "success")

        except IntegrityError:
            connection.rollback()
            flash("That email address is already used by another student.", "error")

        finally:
            cursor.close()
            connection.close()

        return redirect(url_for("index"))

    cursor.execute(
        "SELECT * FROM students WHERE id = %s",
        (student_id,)
    )
    student = cursor.fetchone()

    cursor.close()
    connection.close()

    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("index"))

    return render_template("edit.html", student=student)


# Delete a student
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (student_id,)
    )
    connection.commit()

    if cursor.rowcount > 0:
        flash("Student deleted successfully!", "success")
    else:
        flash("Student not found.", "error")

    cursor.close()
    connection.close()

    return redirect(url_for("index"))


# Start the application
if __name__ == "__main__":
    app.run(debug=True)
