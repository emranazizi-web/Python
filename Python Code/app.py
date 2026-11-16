"""
app.py

This is the main file of the Student Attendance Management System.
It creates the Flask web application. Each "route" below is a web
address. When the browser visits a route, Flask runs the function
under it, which calls methods of the AttendanceSystem class and then
shows an HTML page.

The website is used by the teacher. The teacher can:
* see the courses and add a new course on the Dashboard,
* open a course to mark each student Present, Late or Absent,
* add students to a course or remove them,
* open a student to see their attendance records for that course.

Run the program from the main project folder with:
    python "Python Code/app.py"
Then open http://127.0.0.1:5000 in a web browser.
"""

import os
from datetime import date

from flask import Flask, flash, redirect, render_template, request, \
    send_from_directory, session, url_for

from attendance_system import AttendanceSystem

# The main project folder is one level above this file's folder.
PYTHON_FOLDER = os.path.dirname(os.path.abspath(__file__))
PROJECT_FOLDER = os.path.dirname(PYTHON_FOLDER)

# The folders that hold each type of file.
HTML_FOLDER = os.path.join(PROJECT_FOLDER, "HTML Pages")
CSS_FOLDER = os.path.join(PROJECT_FOLDER, "CSS Design")
JAVASCRIPT_FOLDER = os.path.join(PROJECT_FOLDER, "JavaScript")
DATA_FOLDER = os.path.join(PROJECT_FOLDER, "Data Files")

# Tell Flask where the HTML pages and the CSS file are.
# The CSS file will be available at the web address /css/style.css
app = Flask(__name__, template_folder=HTML_FOLDER,
            static_folder=CSS_FOLDER, static_url_path="/css")

# Flask needs a secret key to remember who is logged in (the "session")
# and to show one-time messages (the "flash" messages).
app.secret_key = "b100-student-attendance-project"

# One AttendanceSystem object is shared by the whole application.
# The CSV files are kept in the "Data Files" folder.
system = AttendanceSystem(DATA_FOLDER)


def is_teacher_logged_in():
    """Return True if the teacher has logged in."""
    return session.get("teacher") is True


def get_course_rows():
    """Return one row of information for each course."""
    course_rows = []
    for course in system.courses:
        course_rows.append({
            "course": course,
            "student_count": course.count_students(system.students),
        })
    return course_rows


@app.route("/javascript/<filename>")
def javascript_file(filename):
    """Send a JavaScript file from the "JavaScript" folder to the browser."""
    return send_from_directory(JAVASCRIPT_FOLDER, filename)


@app.route("/", methods=["GET", "POST"])
def login():
    """Show the login page and check the teacher's login details."""
    if is_teacher_logged_in():
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if system.teacher_login(username, password):
            session["teacher"] = True
            return redirect(url_for("dashboard"))

        flash("Incorrect User ID or password.")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    """Show the list of courses and the form to add a new course."""
    if not is_teacher_logged_in():
        return redirect(url_for("login"))

    return render_template("dashboard.html", course_rows=get_course_rows())


@app.route("/add_course", methods=["POST"])
def add_course():
    """Create a new course from the Dashboard form."""
    if not is_teacher_logged_in():
        return redirect(url_for("login"))

    course_name = request.form.get("course_name", "")
    try:
        course = system.create_course(course_name)
        # f"{course}" uses the Course __str__() method,
        # for example "Web Design (C004)".
        flash(f"The course {course} was added.")
    except ValueError as error:
        flash(str(error))

    return redirect(url_for("dashboard"))


@app.route("/course/<course_code>")
def course_page(course_code):
    """Show the students of one course with Present/Late/Absent options."""
    if not is_teacher_logged_in():
        return redirect(url_for("login"))

    course = system.find_course(course_code)
    if course is None:
        flash("That course does not exist.")
        return redirect(url_for("dashboard"))

    # Use the date from the web address, or today's date.
    selected_date = request.args.get("date", date.today().isoformat())

    # Build one row for each student in the course.
    student_rows = []
    for student in system.get_course_students(course):
        student_rows.append({
            "student": student,
            "saved_status": system.get_saved_status(student, course,
                                                    selected_date),
            "summary": system.get_course_summary(student, course),
        })

    return render_template(
        "course.html",
        course=course,
        selected_date=selected_date,
        student_rows=student_rows,
    )


@app.route("/course/<course_code>/attendance", methods=["POST"])
def save_attendance(course_code):
    """Save Present/Late/Absent for every student in a course."""
    if not is_teacher_logged_in():
        return redirect(url_for("login"))

    course = system.find_course(course_code)
    if course is None:
        return redirect(url_for("dashboard"))

    date_text = request.form.get("date", "")
    try:
        system.check_date(date_text)
    except ValueError as error:
        flash(str(error))
        return redirect(url_for("course_page", course_code=course_code))

    saved_count = 0
    for student in system.get_course_students(course):
        # Each student's option is sent as "status_<student ID>".
        status = request.form.get("status_" + student.student_id, "")
        if status == "":
            continue  # No option was chosen for this student.
        try:
            system.mark_attendance(student, course_code, date_text, status)
            saved_count = saved_count + 1
        except ValueError as error:
            flash(str(error))

    flash(f"Attendance saved for {saved_count} students on {date_text}.")
    return redirect(url_for("course_page", course_code=course_code,
                            date=date_text))


@app.route("/course/<course_code>/add_student", methods=["POST"])
def add_student(course_code):
    """Add a student to a course."""
    if not is_teacher_logged_in():
        return redirect(url_for("login"))

    course = system.find_course(course_code)
    if course is None:
        return redirect(url_for("dashboard"))

    student_id = request.form.get("student_id", "")
    name = request.form.get("name", "")
    try:
        student = system.add_student_to_course(course, student_id, name)
        flash(f"{student.name} was added to {course.course_name}.")
    except ValueError as error:
        flash(str(error))

    return redirect(url_for("course_page", course_code=course_code))


@app.route("/course/<course_code>/remove_student/<student_id>",
           methods=["POST"])
def remove_student(course_code, student_id):
    """Remove a student from a course."""
    if not is_teacher_logged_in():
        return redirect(url_for("login"))

    course = system.find_course(course_code)
    student = system.find_student(student_id)
    if course is None or student is None:
        return redirect(url_for("dashboard"))

    try:
        system.remove_student_from_course(course, student)
        flash(f"{student.name} was removed from {course.course_name}.")
    except ValueError as error:
        flash(str(error))

    return redirect(url_for("course_page", course_code=course_code))


@app.route("/course/<course_code>/student/<student_id>")
def student_page(course_code, student_id):
    """Show the attendance records of one student in one course."""
    if not is_teacher_logged_in():
        return redirect(url_for("login"))

    course = system.find_course(course_code)
    student = system.find_student(student_id)
    if course is None or student is None:
        flash("That course or student does not exist.")
        return redirect(url_for("dashboard"))

    return render_template(
        "student.html",
        student=student,
        course=course,
        summary=system.get_course_summary(student, course),
        records=system.get_student_course_records(student, course),
    )


@app.route("/logout")
def logout():
    """Log the teacher out and go back to the login page."""
    session.clear()
    flash("You have logged out.")
    return redirect(url_for("login"))


# This block only runs when the file is started with "python app.py".
if __name__ == "__main__":
    app.run(debug=True)
