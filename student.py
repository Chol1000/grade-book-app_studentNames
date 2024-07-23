# Import Course class from course.py
from course import Course

class Student:
    def __init__(self, email, names):
        self.email = email
        self.names = names
        self.courses_registered = []  # This will hold Course objects
        self.GPA = 0.0

    def calculate_GPA(self):
        if not self.courses_registered:
            return 0.0
        total_credits = sum(course.credits for course in self.courses_registered)
        total_grade_points = sum(course.credits * course.grade for course in self.courses_registered if course.grade is not None)
        if total_credits == 0:
            return 0.0
        self.GPA = total_grade_points / total_credits
        return self.GPA

    def register_for_course(self, course_name, trimester, credits, grade):
        course = Course(course_name, trimester, credits, grade)  # Instantiate Course object
        self.courses_registered.append(course)

    def to_dict(self):
        return {
            'email': self.email,
            'names': self.names,
            'courses_registered': [course.to_dict() for course in self.courses_registered],
            'GPA': self.GPA
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(data['email'], data['names'])
        student.courses_registered = [Course.from_dict(course_data) for course_data in data['courses_registered']]
        student.GPA = data['GPA']
        return student

