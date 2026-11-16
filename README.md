# 🎓 Student Attendance Management System

A simple web application that helps a teacher **take attendance** for each
course and **view every student's records**.

Created by **Emran Azizi** for the module
**B100 – Introduction to Computer Programming with Python**.

---

## 🌐 Live Website

**👉 https://emranwebsite7.pythonanywhere.com**

| User ID      | Password |
|--------------|----------|
| `Attendance` | `12345`  |

---

## 🛠️ Built With

| Language / Tool | Used for |
|-----------------|----------|
| **Python**      | All program logic: classes, rules and file handling |
| **Flask**       | Connects the web pages to the Python code |
| **HTML**        | The structure of the pages |
| **CSS**         | The design and layout |
| **JavaScript**  | Small checks, such as empty fields and confirming removals |
| **CSV files**   | Saving students, courses and attendance |

---

## ✨ Features

- **Teacher login** with a User ID and password
- **Dashboard** showing all courses, with a form to **add a new course**
- **Course page** where the teacher can:
  - choose a date and mark each student **Present**, **Late** or **Absent**
  - **add** a student to the course or **remove** one
  - open **View Records** for any student
- **Student records page** showing total, present, late and absent classes,
  the attendance percentage, and every record for that course
- **Input checks**: no future dates, no duplicate courses, and a maximum of
  three courses per student
- **All changes are saved** in CSV files

---

## 🐍 Python Requirements Covered

| Requirement | Where |
|-------------|-------|
| 4 classes | `Student`, `Course`, `AttendanceRecord`, `AttendanceSystem` |
| 4+ methods per class | 5, 6, 7 and 24 methods |
| Objects and attributes | e.g. `student.name`, `course.course_code`, `record.status` |
| Loops | `for` loops to load and search data, a `while` loop in `make_course_code()` |
| Conditional statements | `if` / `elif` / `else` for login, dates, statuses and limits |
| File reading and writing | `read_csv_file()` and `write_csv_file()` with the `csv` module |
| Exception handling | `try` / `except` for missing files, bad data and invalid input |
| Multiple modules | 5 Python files that import each other |
| PEP 8 | All Python files pass `pycodestyle` |
| Comments and docstrings | Every module, class and method is documented |
| Interactive functionality | Web forms for every action |

---

## 📁 Project Structure

```
Student_Attendance_System/
├── Python Code/
│   ├── app.py                  # Flask routes (connects pages to Python)
│   ├── attendance_system.py    # AttendanceSystem class – main logic
│   ├── student.py              # Student class
│   ├── course.py               # Course class
│   └── attendance_record.py    # AttendanceRecord class
├── HTML Pages/                 # login, dashboard, course, student pages
├── CSS Design/                 # style.css
├── JavaScript/                 # script.js
└── Data Files/                 # students.csv, courses.csv, attendance.csv
```

---

## 💻 Run on Your Computer

You need **Python 3.10 or newer**.

```bash
pip install flask
python "Python Code/app.py"
```

Then open **http://127.0.0.1:5000** in your browser.

---

## ⚙️ How It Works

1. The teacher clicks a button or submits a form on a web page.
2. Flask (`app.py`) receives it and calls a method of the
   `AttendanceSystem` class.
3. `AttendanceSystem` uses the `Student`, `Course` and `AttendanceRecord`
   objects to apply the rules.
4. The changes are saved to the CSV files in `Data Files`.
5. The updated page is shown with a message such as *"Attendance saved."*
