"""
attendance_record.py

This module contains the AttendanceRecord class.
An AttendanceRecord object stores whether one student was present,
late or absent for one course on one date.
"""


class AttendanceRecord:
    """Represents one attendance entry for a student."""

    # The only statuses that are allowed.
    VALID_STATUSES = ["Present", "Late", "Absent"]

    def __init__(self, student_id, course_code, date, status):
        """Create a new AttendanceRecord object.

        Args:
            student_id (str): The ID of the student, for example "GH1030615".
            course_code (str): The code of the course, for example "C001".
            date (str): The date in the format YYYY-MM-DD.
            status (str): "Present", "Late" or "Absent".

        Raises:
            ValueError: If the status is not one of VALID_STATUSES.
        """
        self.student_id = student_id
        self.course_code = course_code
        self.date = date
        self.status = ""
        self.set_status(status)

    def set_status(self, status):
        """Change the status of this record.

        Raises:
            ValueError: If the status is not one of VALID_STATUSES.
        """
        if status not in AttendanceRecord.VALID_STATUSES:
            raise ValueError("Status must be Present, Late or Absent.")
        self.status = status

    def is_present(self):
        """Return True if the student was present (on time)."""
        return self.status == "Present"

    def is_late(self):
        """Return True if the student came late."""
        return self.status == "Late"

    def belongs_to(self, student_id):
        """Return True if this record belongs to the given student."""
        return self.student_id == student_id

    def is_for_course(self, course_code):
        """Return True if this record is for the given course."""
        return self.course_code == course_code

    def is_same_class(self, student_id, course_code, date):
        """Return True if this record is for the same student, course
        and date.
        """
        return (
            self.belongs_to(student_id)
            and self.is_for_course(course_code)
            and self.date == date
        )

    def to_csv_row(self):
        """Return the record's data as a list, ready to write to a CSV file."""
        return [self.student_id, self.course_code, self.date, self.status]
