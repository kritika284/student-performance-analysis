"""
Student Performance Analysis System
Course: Computational Thinking and Programming
Course Code: 2026CSAE100

A menu-driven Python application that:
- stores student marks in CSV
- validates input
- calculates totals, averages and grades
- ranks students
- identifies weak subjects
- generates class summaries
- exports an automatic text report

The project intentionally uses beginner/intermediate Python concepts
covered in the course rather than advanced AI/ML.
"""

import csv
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("students.csv")
REPORT_FILE = Path("performance_report.txt")

SUBJECTS = ["Mathematics", "Physics", "Programming", "Communication"]


def initialize_data_file():
    """Create the CSV file with sample data if it does not exist."""
    if not DATA_FILE.exists():
        sample_students = [
            {"Name": "Aarav", "RollNo": "101", "Mathematics": 86, "Physics": 78, "Programming": 92, "Communication": 81},
            {"Name": "Diya", "RollNo": "102", "Mathematics": 72, "Physics": 68, "Programming": 85, "Communication": 76},
            {"Name": "Kabir", "RollNo": "103", "Mathematics": 91, "Physics": 88, "Programming": 95, "Communication": 89},
            {"Name": "Meera", "RollNo": "104", "Mathematics": 64, "Physics": 59, "Programming": 71, "Communication": 66},
            {"Name": "Rohan", "RollNo": "105", "Mathematics": 78, "Physics": 74, "Programming": 69, "Communication": 83},
        ]
        write_students(sample_students)


def calculate_total(student):
    """Return total marks across all subjects."""
    return sum(int(student[subject]) for subject in SUBJECTS)


def calculate_average(student):
    """Return average marks across all subjects."""
    return calculate_total(student) / len(SUBJECTS)


def calculate_grade(average):
    """Assign a grade using simple rule-based conditions."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def is_valid_mark(mark):
    """Check whether a mark is an integer from 0 to 100."""
    return 0 <= int(mark) <= 100


def read_students():
    """Read all students from the CSV file."""
    students = []
    try:
        with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                for subject in SUBJECTS:
                    row[subject] = int(row[subject])
                students.append(row)
    except FileNotFoundError:
        initialize_data_file()
        return read_students()
    except (ValueError, KeyError):
        print("Error: students.csv contains invalid or missing data.")
    return students


def write_students(students):
    """Write student records to the CSV file."""
    fieldnames = ["Name", "RollNo"] + SUBJECTS
    with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for student in students:
            writer.writerow({field: student[field] for field in fieldnames})


def add_student():
    """Collect and validate one student record."""
    students = read_students()

    print("\n--- Add Student ---")
    name = input("Student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    roll_no = input("Roll number: ").strip()
    if not roll_no:
        print("Roll number cannot be empty.")
        return

    if any(student["RollNo"] == roll_no for student in students):
        print("A student with this roll number already exists.")
        return

    student = {"Name": name, "RollNo": roll_no}

    for subject in SUBJECTS:
        while True:
            try:
                mark = int(input(f"{subject} marks (0-100): "))
                if is_valid_mark(mark):
                    student[subject] = mark
                    break
                print("Please enter a value from 0 to 100.")
            except ValueError:
                print("Invalid input. Enter a whole number.")

    students.append(student)
    write_students(students)
    print("Student added successfully.")


def display_students():
    """Display all student records with computed results."""
    students = read_students()
    if not students:
        print("No student records available.")
        return

    print("\n--- Student Records ---")
    print("-" * 86)
    print(f"{'Roll':<8}{'Name':<15}{'Total':<10}{'Average':<12}{'Grade':<8}", end="")
    for subject in SUBJECTS:
        print(f"{subject[:8]:<10}", end="")
    print()
    print("-" * 86)

    for student in students:
        total = calculate_total(student)
        average = calculate_average(student)
        grade = calculate_grade(average)
        print(f"{student['RollNo']:<8}{student['Name']:<15}{total:<10}{average:<12.2f}{grade:<8}", end="")
        for subject in SUBJECTS:
            print(f"{student[subject]:<10}", end="")
        print()


def rank_students():
    """Rank students by average marks."""
    students = read_students()
    ranked = sorted(students, key=calculate_average, reverse=True)

    print("\n--- Student Ranking ---")
    if not ranked:
        print("No records available.")
        return

    for position, student in enumerate(ranked, start=1):
        average = calculate_average(student)
        print(f"{position}. {student['Name']} (Roll {student['RollNo']}) - "
              f"Average: {average:.2f} - Grade: {calculate_grade(average)}")


def subject_analysis():
    """Show subject averages and weak-subject information."""
    students = read_students()
    if not students:
        print("No records available.")
        return

    print("\n--- Subject Analysis ---")
    subject_averages = {}

    for subject in SUBJECTS:
        average = sum(student[subject] for student in students) / len(students)
        subject_averages[subject] = average
        print(f"{subject:<18}: {average:.2f}")

    weakest_subject = min(subject_averages, key=subject_averages.get)
    strongest_subject = max(subject_averages, key=subject_averages.get)

    print(f"\nLowest class average : {weakest_subject} ({subject_averages[weakest_subject]:.2f})")
    print(f"Highest class average: {strongest_subject} ({subject_averages[strongest_subject]:.2f})")

    print("\nStudents needing attention (any subject below 50):")
    found = False
    for student in students:
        weak = [subject for subject in SUBJECTS if student[subject] < 50]
        if weak:
            found = True
            print(f"- {student['Name']}: {', '.join(weak)}")
    if not found:
        print("- None in the current dataset.")


def student_summary():
    """Show detailed analysis for one roll number."""
    students = read_students()
    roll_no = input("\nEnter roll number: ").strip()

    student = next((s for s in students if s["RollNo"] == roll_no), None)
    if student is None:
        print("Student not found.")
        return

    total = calculate_total(student)
    average = calculate_average(student)
    grade = calculate_grade(average)

    print(f"\n--- Summary for {student['Name']} ---")
    print(f"Roll number: {student['RollNo']}")
    for subject in SUBJECTS:
        print(f"{subject}: {student[subject]}")
    print(f"Total: {total}/{len(SUBJECTS) * 100}")
    print(f"Average: {average:.2f}")
    print(f"Grade: {grade}")

    weak_subjects = [s for s in SUBJECTS if student[s] < 60]
    if weak_subjects:
        print("Improvement areas:", ", ".join(weak_subjects))
    else:
        print("Improvement areas: No subject below 60.")


def generate_report():
    """Generate a text report containing computed class statistics."""
    students = read_students()
    if not students:
        print("No records available.")
        return

    class_average = sum(calculate_average(s) for s in students) / len(students)
    ranked = sorted(students, key=calculate_average, reverse=True)
    subject_averages = {
        subject: sum(s[subject] for s in students) / len(students)
        for subject in SUBJECTS
    }

    with REPORT_FILE.open("w", encoding="utf-8") as file:
        file.write("STUDENT PERFORMANCE ANALYSIS REPORT\n")
        file.write("=" * 42 + "\n")
        file.write(f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n")
        file.write(f"Number of students: {len(students)}\n")
        file.write(f"Class average: {class_average:.2f}\n\n")

        file.write("TOP STUDENTS\n")
        file.write("-" * 20 + "\n")
        for position, student in enumerate(ranked[:3], start=1):
            file.write(
                f"{position}. {student['Name']} | "
                f"Average: {calculate_average(student):.2f} | "
                f"Grade: {calculate_grade(calculate_average(student))}\n"
            )

        file.write("\nSUBJECT AVERAGES\n")
        file.write("-" * 20 + "\n")
        for subject, average in subject_averages.items():
            file.write(f"{subject}: {average:.2f}\n")

        file.write("\nIMPROVEMENT AREAS\n")
        file.write("-" * 20 + "\n")
        for student in students:
            weak = [subject for subject in SUBJECTS if student[subject] < 60]
            if weak:
                file.write(f"{student['Name']}: {', '.join(weak)}\n")

    print(f"Report generated successfully: {REPORT_FILE}")


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 55)
    print(" STUDENT PERFORMANCE ANALYSIS SYSTEM")
    print("=" * 55)
    print("1. Display all students")
    print("2. Add a student")
    print("3. Rank students")
    print("4. Subject analysis")
    print("5. Individual student summary")
    print("6. Generate performance report")
    print("7. Exit")
    print("=" * 55)


def main():
    initialize_data_file()

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            display_students()
        elif choice == "2":
            add_student()
        elif choice == "3":
            rank_students()
        elif choice == "4":
            subject_analysis()
        elif choice == "5":
            student_summary()
        elif choice == "6":
            generate_report()
        elif choice == "7":
            print("Thank you for using the Student Performance Analysis System.")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()
