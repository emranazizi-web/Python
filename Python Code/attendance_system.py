"""
attendance_system.py

This module contains the AttendanceSystem class.
The AttendanceSystem is the "manager" of the program. It:

* reads the students, courses and attendance records from CSV files,
* keeps them in lists of Student, Course and AttendanceRecord objects,
* carries out actions such as adding a course, adding a student to a
  course and marking attendance,
* writes any changes back to the CSV files.
"""

import csv
import os
from datetime import date, datetime

from attendance_record import AttendanceRecord
from course import Course
from student import Student


class AttendanceSystem:
    """Manages all students, courses and attendance records."""

    # The first line (header) of each CSV file.
    STUDENT_HEADER = ["student_id", "name", "courses"]
    COURSE_HEADER = ["course_code", "course_name"]
    ATTENDANCE_HEADER = ["student_id", "course_code", "date", "status"]

    # The login details of the teacher, who uses the website.
    TEACHER_USERNAME = "Attendance"
    TEACHER_PASSWORD = "12345"

    def __init__(self, data_folder):
        """Create the system and load all data from the CSV files.

        Args:
            data_folder (str): The folder that holds the CSV files.
        """
        self.students_file = os.path.join(data_folder, "students.csv")
        self.courses_file = os.path.join(data_folder, "courses.csv")
        self.attendance_file = os.path.join(data_folder, "attendance.csv")

        self.students = []
        self.courses = []
        self.records = []

        self.load_students()
        self.load_courses()
        self.load_attendance()

    # ------------------------------------------------------------------
    # Reading and writing CSV files
    # ------------------------------------------------------------------

    def read_csv_file(self, file_path):
        """Read a CSV file and return its rows as a list of lists.

        The header line is skipped. If the file does not exist, a
        warning is printed and an empty list is returned.
        """
        rows = []
        try:
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip the header line.
                for row in reader:
                    if row:  # Ignore empty lines.
                        rows.append(row)
        except FileNotFoundError:
            print(f"Warning: {file_path} was not found.")
        return rows

    def write_csv_file(self, file_path, header, rows):
        """Write a header and a list of rows to a CSV file.

        Raises:
            ValueError: If the file could not be written.
        """
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(rows)
        except OSError:
            raise ValueError("Sorry, the data could not be saved.")

    def load_students(self):
        """Create a Student object for each row in students.csv."""
        for row in self.read_csv_file(self.students_file):
            try:
                student_id, name, courses_text = row
            except ValueError:
                print(f"Skipping a badly formatted student row: {row}")
                continue

            # "C001;C002" becomes ["C001", "C002"]. An empty text
            # becomes an empty list.
            if courses_text == "":
                course_codes = []
            else:
                course_codes = courses_text.split(";")

            self.students.append(Student(student_id, name, course_codes))

    def load_courses(self):
        """Create a Course object for each row in courses.csv."""
        for row in self.read_csv_file(self.courses_file):
            if len(row) != 2:
                print(f"Skipping a badly formatted course row: {row}")
                continue
            self.courses.append(Course(row[0], row[1]))

    def load_attendance(self):
        """Create an AttendanceRecord object for each row in attendance.csv."""
        for row in self.read_csv_file(self.attendance_file):
            try:
                student_id, course_code, class_date, status = row
                record = AttendanceRecord(student_id, course_code,
                                          class_date, status)
            except ValueError:
                print(f"Skipping a badly formatted attendance row: {row}")
                continue
            self.records.append(record)

    def save_students(self):
        """Write every student back to students.csv."""
        rows = []
        for student in self.students:
            rows.append(student.to_csv_row())
        self.write_csv_file(self.students_file,
                            AttendanceSystem.STUDENT_HEADER, rows)

    def save_courses(self):
        """Write every course back to courses.csv."""
        rows = []
        for course in self.courses:
            rows.append(course.to_csv_row())
        self.write_csv_file(self.courses_file,
                            AttendanceSystem.COURSE_HEADER, rows)

    def save_attendance(self):
        """Write every attendance record back to attendance.csv."""
        rows = []
        for record in self.records:
            rows.append(record.to_csv_row())
        self.write_csv_file(self.attendance_file,
                            AttendanceSystem.ATTENDANCE_HEADER, rows)

    # ------------------------------------------------------------------
    # Login and finding students and courses
    # ------------------------------------------------------------------

    def teacher_login(self, username, password):
        """Return True if the teacher's username and password are correct.

        The username is not case-sensitive, so "Attendance" and
        "attendance" both work.
        """
        correct_username = AttendanceSystem.TEACHER_USERNAME.lower()
        if username.lower() == correct_username and \
                password == AttendanceSystem.TEACHER_PASSWORD:
            return True
        return False

    def find_student(self, student_id):
        """Return the Student with the given ID, or None if not found."""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def find_course(self, course_code):
        """Return the Course with the given code, or None if not found."""
        for course in self.courses:
            if course.matches(course_code):
                return course
        return None

    def get_course_students(self, course):
        """Return a list of the Student objects registered for a course."""
        course_students = []
        for student in self.students:
            if course.is_taken_by(student):
                course_students.append(student)
        return course_students

    # ------------------------------------------------------------------
    # Managing courses and students
    # ------------------------------------------------------------------

    def make_course_code(self):
        """Return a new, unused course code such as "C004"."""
        number = len(self.courses) + 1
        code = "C" + str(number).zfill(3)  # zfill(3) turns 4 into "004"

        # If the code is already used, try the next number.
        while self.find_course(code) is not None:
            number = number + 1
            code = "C" + str(number).zfill(3)

        return code

    def create_course(self, course_name):
        """Create a new course and save it to courses.csv.

        Returns:
            Course: The new course.

        Raises:
            ValueError: If the name is empty or the course already exists.
        """
        course_name = course_name.strip()
        if course_name == "":
            raise ValueError("Please enter a course name.")

        for course in self.courses:
            if course.has_name(course_name):
                raise ValueError(f"The course {course_name} already exists.")

        new_course = Course(self.make_course_code(), course_name)
        self.courses.append(new_course)
        self.save_courses()
        return new_course

    def add_student_to_course(self, course, student_id, name):
        """Add a student to a course and save the change.

        If no student has this ID yet, a new student is created with
        the given name.

        Returns:
            Student: The student who was added.

        Raises:
            ValueError: If the details are missing or the student
                cannot be added to the course.
        """
        student_id = student_id.strip()
        name = name.strip()

        if student_id == "":
            raise ValueError("Please enter the student ID.")

        student = self.find_student(student_id)

        if student is None:
            # This is a new student, so a name is needed.
            if name == "":
                raise ValueError("Please enter the name of the new student.")
            student = Student(student_id, name, [])
            student.add_course(course.course_code)
            self.students.append(student)
        else:
            student.add_course(course.course_code)

        self.save_students()
        return student

    def remove_student_from_course(self, course, student):
        """Remove a student from a course and save the change.

        Old attendance records for the course are kept.

        Raises:
            ValueError: If the student is not in the course.
        """
        student.remove_course(course.course_code)
        self.save_students()

    # ------------------------------------------------------------------
    # Attendance
    # ------------------------------------------------------------------

    def check_date(self, date_text):
        """Check that the date is real and not in the future.

        Raises:
            ValueError: If the date is not valid.
        """
        try:
            class_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Please enter a valid date.")

        if class_date > date.today():
            raise ValueError("You cannot mark attendance for a future date.")

    def find_record(self, student_id, course_code, date_text):
        """Return the record for this student, course and date, or None."""
        for record in self.records:
            if record.is_same_class(student_id, course_code, date_text):
                return record
        return None

    def mark_attendance(self, student, course_code, date_text, status):
        """Save a student's attendance for one class.

        If attendance was already saved for that class, the status is
        changed instead, so the teacher can correct mistakes.

        Raises:
            ValueError: If the course, date or status is not valid.
        """
        if not student.is_registered(course_code):
            raise ValueError(f"{student.name} is not in this course.")

        self.check_date(date_text)

        record = self.find_record(student.student_id, course_code, date_text)
        if record is None:
            record = AttendanceRecord(student.student_id, course_code,
                                      date_text, status)
            self.records.append(record)
        else:
            record.set_status(status)

        self.save_attendance()

    def get_saved_status(self, student, course, date_text):
        """Return the saved status for one class, or "" if none is saved."""
        record = self.find_record(student.student_id, course.course_code,
                                  date_text)
        if record is None:
            return ""
        return record.status

    def get_student_records(self, student):
        """Return a list of all attendance records for one student."""
        student_records = []
        for record in self.records:
            if record.belongs_to(student.student_id):
                student_records.append(record)
        return student_records

    def get_student_course_records(self, student, course):
        """Return a list of one student's records in one course only."""
        course_records = []
        for record in self.get_student_records(student):
            if record.is_for_course(course.course_code):
                course_records.append(record)
        return course_records

    def count_records(self, records):
        """Count the Present, Late and Absent records in a list.

        Late counts as attended when the percentage is worked out.

        Returns:
            dict: The total, present, late and absent classes and the
                attendance percentage.
        """
        present = 0
        late = 0
        absent = 0

        for record in records:
            if record.is_present():
                present = present + 1
            elif record.is_late():
                late = late + 1
            else:
                absent = absent + 1

        total = present + late + absent

        # Avoid dividing by zero when there are no classes yet.
        if total == 0:
            percentage = 0.0
        else:
            percentage = round((present + late) / total * 100, 1)

        return {
            "total": total,
            "present": present,
            "late": late,
            "absent": absent,
            "percentage": percentage,
        }

    def get_course_summary(self, student, course):
        """Count the classes for one student in one course."""
        course_records = self.get_student_course_records(student, course)
        return self.count_records(course_records)
