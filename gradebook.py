#!/usr/bin/python3
from student import Student
from course import Course
import json

# Initialize global variables
student_list = []
course_list = []  # Added course_list initialization

# Function to add a new student
def add_student():
    email = input("Enter student's email: ")
    names = input("Enter student's names: ")
    student = Student(email, names)
    student_list.append(student)
    print(f"Student {names} added successfully.")

# Function to add a new course
def add_course():
    course_name = input("Enter course name: ")
    trimester = input("Enter trimester: ")
    credits = float(input("Enter credits: "))
    course = Course(course_name, trimester, credits)
    course_list.append(course)  # Fixed: course_list was not defined before
    print(f"Course {course_name} added successfully.")

# Function to register a student for a course
def register_student_for_course():
    email = input("Enter student's email: ")
    course_name = input("Enter course name to register: ")
    trimester = input("Enter trimester: ")
    credits = float(input("Enter credits: "))
    grade = float(input("Enter grade for the course (or enter 0.0 if not graded): "))  # Prompt for grade

    # Find the student in student_list
    for student in student_list:
        if student.email == email:
            # Register student for course with grade
            student.register_for_course(course_name, trimester, credits, grade)
            print(f"Student {student.names} registered for {course_name} with grade {grade} successfully.")
            return
    
    print(f"Student with email {email} not found.")

# Function to calculate GPA for a student
def calculate_GPA():
    email = input("Enter student's email to calculate GPA: ")

    # Find the student in student_list
    for student in student_list:
        if student.email == email:
            GPA = student.calculate_GPA()
            print(f"GPA calculated for {student.names}: {GPA}")
            return
    
    print(f"Student with email {email} not found.")

# Function to calculate ranking based on GPA
def calculate_ranking():
    ranked_students = sorted(student_list, key=lambda student: student.GPA, reverse=True)
    for rank, student in enumerate(ranked_students, start=1):
        print(f"Rank {rank}: Email: {student.email}, GPA: {student.GPA}")

# Function to search students by grade range
def search_by_grade_range():
    min_GPA = float(input("Enter minimum GPA: "))
    max_GPA = float(input("Enter maximum GPA: "))

    filtered_students = [student for student in student_list if min_GPA <= student.GPA <= max_GPA]
    print("Students in grade range:")
    if filtered_students:
        for student in filtered_students:
            print(f"Email: {student.email}, GPA: {student.GPA}")
    else:
        print("No students found in the specified grade range.")

# Function to generate transcript for a student
def generate_transcript():
    email = input("Enter student's email for transcript: ")

    # Find the student in student_list
    for student in student_list:
        if student.email == email:
            print(f"Transcript for {student.names}:")
            print(f"Email: {student.email}")
            print(f"GPA: {student.GPA}")
            print("Courses:")
            for course in student.courses_registered:
                print(f"- {course.name} ({course.trimester}) - Credits: {course.credits}")
            return
    
    print(f"Student with email {email} not found.")

# Function to print all students
def print_all_students():
    if student_list:
        for student in student_list:
            print(f"Email: {student.email}, Names: {student.names}, GPA: {student.GPA}")
    else:
        print("No student records.")

# Main menu function
def main_menu():
    while True:
        print("\n=== Grade Book Application Menu ===")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Register Student for Course")
        print("4. Calculate GPA")
        print("5. Calculate Ranking")
        print("6. Search by Grade Range")
        print("7. Generate Transcript")
        print("8. Print All Students")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            add_student()
        elif choice == '2':
            add_course()
        elif choice == '3':
            register_student_for_course()
        elif choice == '4':
            calculate_GPA()
        elif choice == '5':
            calculate_ranking()
        elif choice == '6':
            search_by_grade_range()
        elif choice == '7':
            generate_transcript()
        elif choice == '8':
            print_all_students()
        elif choice == '9':
            print("Exiting Grade Book Application.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")

# Entry point of the application
if __name__ == "__main__":
    main_menu()

