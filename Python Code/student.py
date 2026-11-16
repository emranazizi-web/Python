"""
student.py

This module contains the Student class.
A Student object stores the details of one student and the codes
of the courses that the student is registered for.
"""


class Student:
    """Represents one student in the attendance system."""

    # The largest number of courses a student may register for.
    # This is a class attribute, so it is shared by every Student object.
    MAX_COURSES = 3

    def __init__(self, student_id, name, course_codes):
        """Create a new Student object.

        Args:
            student_id (str): The student's ID, for example "GH1030615".
            name (str): The student's full name.
            course_codes (list): Codes of the registered courses,
                for example ["C001", "C002"].
        """
        self.student_id = student_id
        self.name = name
        self.course_codes = course_codes

    def is_registered(self, course_code):
        """Return True if the student is registered for the course."""
        return course_code in self.course_codes

    def can_add_course(self):
        """Return True if the student has fewer than MAX_COURSES courses."""
        return len(self.course_codes) < Student.MAX_COURSES

    def add_course(self, course_code):
        """Register the student for a course.

        Raises:
            ValueError: If the student already has the course or
                has reached the maximum number of courses.
        """
        if self.is_registered(course_code):
            raise ValueError(
                f"{self.name} is already registered for this course."
            )

        if not self.can_add_course():
            raise ValueError(
                f"{self.name} cannot register for more than "
                f"{Student.MAX_COURSES} courses."
            )

        self.course_codes.append(course_code)

    def remove_course(self, course_code):
        """Remove a course from the student's registered courses.

        Raises:
            ValueError: If the student is not registered for the course.
        """
        if not self.is_registered(course_code):
            raise ValueError(
                f"{self.name} is not registered for this course."
            )

        self.course_codes.remove(course_code)

    def to_csv_row(self):
        """Return the student's data as a list, ready to write to a CSV file.

        The course codes are joined with ";" so they fit in one column,
        for example "C001;C002".
        """
        courses_text = ";".join(self.course_codes)
        return [self.student_id, self.name, courses_text]
