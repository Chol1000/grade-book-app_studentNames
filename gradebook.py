#!/usr/bin/python3
import sqlite3
from student import Student
from course import Course

# Initialize SQLite connection and cursor
conn = sqlite3.connect('gradebook.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        email TEXT PRIMARY KEY,
        names TEXT NOT NULL,
        GPA REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        trimester TEXT,
        credits REAL,
        grade REAL,
        student_email TEXT,
        FOREIGN KEY (student_email) REFERENCES students (email)
    )
''')

# Function to add a new student
def add_student():
    email = input("Enter student's email: ")
    names = input("Enter student's names: ")
    student = Student(email, names)
    cursor.execute('INSERT OR IGNORE INTO students (email, names) VALUES (?, ?)', (email, names))
    conn.commit()
    print(f"Student {names} added successfully.")

# Function to add a new course
def add_course():
    course_name = input("Enter course name: ")
    trimester = input("Enter trimester: ")
    credits = float(input("Enter credits: "))
    course = Course(course_name, trimester, credits)
    cursor.execute('INSERT INTO courses (name, trimester, credits) VALUES (?, ?, ?)', (course_name, trimester, credits))
    conn.commit()
    print(f"Course {course_name} added successfully.")

# Function to register a student for a course
def register_student_for_course():
    email = input("Enter student's email: ")
    course_name = input("Enter course name to register: ")
    trimester = input("Enter trimester: ")
    credits = float(input("Enter credits: "))
    grade = float(input("Enter grade for the course (or enter 0.0 if not graded): "))  # Prompt for grade

    cursor.execute('SELECT email FROM students WHERE email = ?', (email,))
    student = cursor.fetchone()
    if student:
        cursor.execute('INSERT INTO courses (name, trimester, credits, grade, student_email) VALUES (?, ?, ?, ?, ?)',
                       (course_name, trimester, credits, grade, email))
        conn.commit()
        print(f"Student with email {email} registered for {course_name} with grade {grade} successfully.")
    else:
        print(f"Student with email {email} not found.")

# Function to calculate GPA for a student
def calculate_GPA():
    email = input("Enter student's email to calculate GPA: ")

    cursor.execute('SELECT * FROM courses WHERE student_email = ?', (email,))
    courses = cursor.fetchall()
    if not courses:
        print(f"No courses found for student with email {email}.")
        return

    total_credits = sum(course[3] for course in courses if course[4] is not None)  # credits is at index 3
    total_grade_points = sum(course[4] * course[3] for course in courses if course[4] is not None)  # grade is at index 4

    if total_credits == 0:
        print(f"No credits found for student with email {email}.")
        return

    GPA = total_grade_points / total_credits

    # Update the GPA in the students table
    cursor.execute('UPDATE students SET GPA = ? WHERE email = ?', (GPA, email))
    conn.commit()

    print(f"GPA calculated for student with email {email}: {GPA:.2f}")

# Function to calculate ranking based on GPA
def calculate_ranking():
    cursor.execute('SELECT * FROM students ORDER BY GPA DESC')
    ranked_students = cursor.fetchall()
    if not ranked_students:
        print("No students found.")
        return

    for rank, student in enumerate(ranked_students, start=1):
        print(f"Rank {rank}: Email: {student[0]}, Names: {student[1]}, GPA: {student[2]}")

# Function to search students by grade range
def search_by_grade_range():
    min_GPA = float(input("Enter minimum GPA: "))
    max_GPA = float(input("Enter maximum GPA: "))

    cursor.execute('SELECT * FROM students WHERE GPA BETWEEN ? AND ?', (min_GPA, max_GPA))
    filtered_students = cursor.fetchall()
    if not filtered_students:
        print("No students found in the specified grade range.")
        return

    print("Students in grade range:")
    for student in filtered_students:
        print(f"Email: {student[0]}, Names: {student[1]}, GPA: {student[2]}")

# Function to generate transcript for a student
def generate_transcript():
    email = input("Enter student's email for transcript: ")

    cursor.execute('SELECT * FROM students WHERE email = ?', (email,))
    student = cursor.fetchone()
    if not student:
        print(f"Student with email {email} not found.")
        return

    print(f"Transcript for {student[1]}:")
    print(f"Email: {student[0]}")
    print(f"GPA: {student[2]}")

    cursor.execute('SELECT * FROM courses WHERE student_email = ?', (email,))
    courses = cursor.fetchall()
    if not courses:
        print(f"No courses found for student with email {email}.")
        return

    print("Courses:")
    for course in courses:
        print(f"- {course[1]} ({course[2]}) - Credits: {course[3]}, Grade: {course[4]}")

# Function to print all students
def print_all_students():
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    if not students:
        print("No student records.")
        return

    for student in students:
        print(f"Email: {student[0]}, Names: {student[1]}, GPA: {student[2]}")

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

# Close database connection
conn.close()

