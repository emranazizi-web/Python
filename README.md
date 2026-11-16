# Student Attendance Management System

A simple web application, written in Python with Flask, that lets a teacher
take attendance for each course and see every student's records.

This project was created for the **B100 Introduction to Computer Programming
with Python** module.

## Project Purpose

The website is used by the teacher. The teacher can:

- log in with a User ID and password,
- see all courses on the Dashboard and add a new course,
- open a course and mark each student **Present**, **Late** or **Absent**,
- add students to a course or remove them,
- see a student's attendance records for a course.

The website is designed for computer browsers (not phones).

All data is stored in CSV files, so no database is needed.

## Login

| User ID    | Password |
|------------|----------|
| Attendance | 12345    |

## Features

- **Login page** – the teacher logs in with the User ID and password.
- **Dashboard** – shows all courses, with an **Open Course** button for each,
  and a form to **add a new course**.
- **Course page** – shows every student in the course. In front of each
  student's name and ID:
  - **Present / Late / Absent** options, saved for the chosen date,
  - the student's attendance percentage,
  - a **View Records** button,
  - a **Remove** button.

  The page also has a form to **add a student**.
- **Student records page** – shows the student's total, present, late and
  absent classes and percentage, and every record, **for that course only**.
- **Input checks** – the system refuses empty logins, invalid or future dates,
  empty course names, duplicate courses, and a student joining more than
  three courses. Saving attendance again for the same date updates it.

Late counts as attended when the attendance percentage is worked out.

## Courses

| Code | Course Name |
|------|-------------|
| C001 | Python Programming |
| C002 | Data Structures and Algorithms |
| C003 | Database and Big Data |

## Students

| Name        | Student ID |
|-------------|------------|
| Emran Azizi | GH1030615  |
| Student 2   | GH2000000  |
| Student 3   | GH3000000  |

## Project Structure

```
Student_Attendance_System/
│
├── Python Code/
│   ├── app.py                 # Flask web application (connects pages to Python)
│   ├── attendance_system.py   # AttendanceSystem class (main program logic)
│   ├── student.py             # Student class
│   ├── course.py              # Course class
│   └── attendance_record.py   # AttendanceRecord class
│
├── HTML Pages/
│   ├── login.html             # Login page
│   ├── dashboard.html         # List of courses and Add Course form
│   ├── course.html            # Take attendance, add or remove students
│   └── student.html           # One student's records in one course
│
├── CSS Design/
│   └── style.css              # Colours and layout of the pages
│
├── JavaScript/
│   └── script.js              # Small checks on the pages
│
├── Data Files/
│   ├── students.csv           # Students and the courses they are in
│   ├── courses.csv            # All courses
│   └── attendance.csv         # All attendance records
│
├── README.md                  # This file
├── requirements.txt           # List of packages to install (Flask)
└── Start Website.bat          # Double-click to start the website (Windows)
```

## Installation

You need **Python 3.10 or newer**.

1. Download or clone this project and open a terminal in the
   `Student_Attendance_System` folder.

2. Create a virtual environment (a private folder for this project's
   packages):

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - Windows: `venv\Scripts\activate`
   - macOS / Linux: `source venv/bin/activate`

4. Install Flask:

   ```bash
   pip install -r requirements.txt
   ```

## How to Run

**Easy way (Windows):** double-click **`Start Website.bat`**. The website
starts and opens in your browser. Close the black window to stop it.

**Or with the terminal:**

1. With the virtual environment active, run this from the
   `Student_Attendance_System` folder:

   ```bash
   python "Python Code/app.py"
   ```

2. Open a web browser and go to **http://127.0.0.1:5000**

3. Log in with User ID `Attendance` and password `12345`.

4. To stop the program, press `Ctrl + C` in the terminal.

## How the Program Works

1. The browser shows an HTML page from the `HTML Pages` folder.
2. When the teacher clicks a button or submits a form, the browser sends it
   to a route in `app.py`.
3. The route calls a method of the `AttendanceSystem` object, for example
   `create_course()`, `add_student_to_course()` or `mark_attendance()`.
4. `AttendanceSystem` uses the `Student`, `Course` and `AttendanceRecord`
   objects, and saves any changes to the CSV files.
5. Flask shows the updated page with a message such as "Attendance saved."

## Python Concepts Used

This table shows where each assignment requirement can be found.

| # | Requirement | Where it is used |
|---|-------------|------------------|
| 1 | At least four classes | `Student` (student.py), `Course` (course.py), `AttendanceRecord` (attendance_record.py), `AttendanceSystem` (attendance_system.py) |
| 2 | At least four methods per class | See the table below: 5, 6, 7 and 24 methods |
| 3 | Objects and attributes | Every student, course and record is an object with attributes, e.g. `student.name`, `student.course_codes`, `course.course_code`, `record.status`. Class attributes: `Student.MAX_COURSES`, `AttendanceRecord.VALID_STATUSES` |
| 4 | Loops | `for` loops to load the CSV files, search lists and count attendance (e.g. `count_records()`, `find_student()`); a `while` loop in `make_course_code()` |
| 5 | Conditional statements | `if` / `elif` / `else` in `count_records()` (Present / Late / Absent), `add_course()` (3-course limit), `check_date()` (future dates), `teacher_login()` |
| 6 | File reading and writing | `read_csv_file()` and `write_csv_file()` in attendance_system.py use the `csv` module with `open()` |
| 7 | Exception handling | `try` / `except FileNotFoundError` (missing file), `except OSError` (cannot save), `except ValueError` (bad CSV rows, invalid dates, rule errors). Methods `raise ValueError` and app.py catches it to show a message |
| 8 | Multiple Python modules | Five files: app.py imports attendance_system.py, which imports student.py, course.py and attendance_record.py |
| 9 | PEP 8 standards | All Python files pass the `pycodestyle` checker with no errors |
| 10 | Comments and docstrings | Every module, class, method and function has a docstring, plus comments that explain the steps |
| 11 | Interactive functionality | The teacher uses web forms to log in, add courses, add and remove students, and mark attendance; every action shows a message |

### Classes and Methods

| Class | Methods (not counting `__init__`) |
|-------|-----------------------------------|
| `Student` (5) | `is_registered()`, `can_add_course()`, `add_course()`, `remove_course()`, `to_csv_row()` |
| `Course` (6) | `matches()`, `has_name()`, `is_taken_by()`, `count_students()`, `to_csv_row()`, `__str__()` |
| `AttendanceRecord` (7) | `set_status()`, `is_present()`, `is_late()`, `belongs_to()`, `is_for_course()`, `is_same_class()`, `to_csv_row()` |
| `AttendanceSystem` (24) | **Files:** `read_csv_file()`, `write_csv_file()`, `load_students()`, `load_courses()`, `load_attendance()`, `save_students()`, `save_courses()`, `save_attendance()`<br>**Finding:** `teacher_login()`, `find_student()`, `find_course()`, `get_course_students()`<br>**Managing:** `make_course_code()`, `create_course()`, `add_student_to_course()`, `remove_student_from_course()`<br>**Attendance:** `check_date()`, `find_record()`, `mark_attendance()`, `get_saved_status()`, `get_student_records()`, `get_student_course_records()`, `count_records()`, `get_course_summary()` |

To check PEP 8 yourself:

```bash
pip install pycodestyle
pycodestyle "Python Code"
```

## Limitations

This is a learning project, so it is kept simple:

- The teacher's login details are written in `attendance_system.py`.
  A real system would store them securely.
- The secret key in `app.py` is written in the code. A real system would keep
  it private.
