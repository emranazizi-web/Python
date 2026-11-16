"""
course.py

This module contains the Course class.
A Course object stores the code and name of one course.
"""


class Course:
    """Represents one course that students can register for."""

    def __init__(self, course_code, course_name):
        """Create a new Course object.

        Args:
            course_code (str): The course code, for example "C001".
            course_name (str): The course name, for example
                "Python Programming".
        """
        self.course_code = course_code
        self.course_name = course_name

    def matches(self, course_code):
        """Return True if this course has the given course code."""
        return self.course_code == course_code

    def has_name(self, course_name):
        """Return True if this course has the given name.

        Capital letters are ignored, so "web design" matches "Web Design".
        """
        return self.course_name.lower() == course_name.lower()

    def is_taken_by(self, student):
        """Return True if the given Student is registered for this course."""
        return student.is_registered(self.course_code)

    def count_students(self, students):
        """Return how many students in the given list take this course."""
        count = 0
        for student in students:
            if self.is_taken_by(student):
                count = count + 1
        return count

    def to_csv_row(self):
        """Return the course's data as a list, ready to write to a CSV file."""
        return [self.course_code, self.course_name]

    def __str__(self):
        """Return a readable description, for example
        "Python Programming (C001)".

        Python calls this method automatically when the object is
        printed or turned into a string with str().
        """
        return f"{self.course_name} ({self.course_code})"
