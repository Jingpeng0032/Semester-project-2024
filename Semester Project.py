import csv
class Course:
    def __init__(self, code, name, credits, students=None, time_slots=None, max_students = 50):
        self.code = code
        self.name = name
        self.credits = credits
        self.students = students if students is not None else []
        self.time_slots = time_slots if time_slots is not None else []
        self.max_students = max_students

    def register_student(self, student, time_slot):
        if len(self.students) >= self.max_students:
            print(f"Cannot register {student.name} for {self.name}: course is full")
        else:
            self.students.append(student)
            self.time_slots.append(time_slot)
            print(f"{student.name} registered for {self.name} ({time_slot})")

    def drop_student(self, student):
        if student in self.students:
            self.students.remove(student)
            print(f"{student.name} dropped from {self.name}")
        else:
            print(f"{student.name} is not enrolled in {self.name}")


    def __str__(self):
        return f"{self.code}: {self.name} ({self.credits} credits)"

    def add_time_slots(self, *time_slots):
        self.time_slots.extend(time_slots)

class MajorCourse(Course):
    def __init__(self, code, name, credits, students=None, prerequisites=None):
        super().__init__(code, name, credits, students)
        self.prerequisites = prerequisites if prerequisites is not None else []

    def add_prerequisite(self, course):
        self.prerequisites.append(course)

    def __str__(self):
        return super().__str__() + " (Required)"


class ElectiveCourse(Course):
    def __str__(self):
        return super().__str__() + " (Elective)"


class Student:
    def __init__(self, name, major, student_id, courses=None, schedule=None):
        self.name = name
        self.major = major
        self.student_id = student_id
        self.completed_courses = []
        self.courses = courses if courses is not None else []
        self.schedule = schedule if schedule is not None else {}

    def register_course(self, course, time_slot):
        total_credits = sum(course.credits for course in self.courses) + course.credits
        if total_credits > 18:
            print(f"{self.name} cannot register for {course}: exceeds credit limit")
        else:
            self.courses.append(course)
            course.register_student(self, time_slot)
            self.schedule[course] = time_slot

    def drop_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
            course.drop_student(self)
            del self.schedule[course]
        else:
            print(f"{self.name} is not enrolled in {course}")

    def get_registered_courses(self):
        return [str(course) for course in self.courses]

    def get_total_credits(self):
        return sum(course.credits for course in self.courses)

    def __str__(self):
        return f"Name: {self.name}\nMajor: {self.major}\nStudent ID: {self.student_id}"


## Define courses for each major
chemical_engineering_courses = [
    MajorCourse("CHEM 2531", "General Chem", 4, prerequisites=None),
]

civil_and_environmental_engineering_courses = [
    MajorCourse("GE 2520", "Structural Analysis", 4, prerequisites=None),
]

computer_science_courses = [
    MajorCourse("CS 2150", "Data Structures and Algorithms", 4, prerequisites=None),
]

electrical_engineering_courses = [
    MajorCourse("EE 2530", "Digital Logic Design", 4, prerequisites=None),
]

physics_courses = [
    MajorCourse("PHS 1990", "Quantum Physics", 4, prerequisites=None),
]


computer_and_electrical_engineering_courses = [
    MajorCourse("EECE 2540", "EECE Fund", 4, prerequisites=["EECE 2530"]),
]
all_elective_courses = [
    ElectiveCourse("EECE 2140", "Computing Fundamentals for Engineers", 4),
    ElectiveCourse("CS 2533", "Digital Logic Design", 1),
    ElectiveCourse("GE 2413", "Energy Systems", 1),
    ElectiveCourse("GE 1990", "Introduction to Engineering", 4),
    ElectiveCourse("EE 2530", "Signal Logic Design", 4),
    ElectiveCourse("CS 2150", "Data Structures", 1),
    ElectiveCourse("EECE 2530", "Circuit Logic Design", 4),
    ElectiveCourse("GE 2413", "Energy Systems", 1),
    ElectiveCourse("MATH 2520", "Structural Analysis", 1),
    ElectiveCourse("GE 1501", "Cornerstone of Engineering", 4),
    ElectiveCourse("GE 2531", "Transport Phenomena", 1),
    ElectiveCourse("EECE 2532", "CIrcuit Design", 1),
    ElectiveCourse("MATH 2413", "Cal3", 4),
    ElectiveCourse("CS 2155", "Data Algorithms", 4),

]


all_major_courses = {
    "Chemical Engineering": chemical_engineering_courses,
    "Computer and Electrical Engineering": computer_and_electrical_engineering_courses,
    'Physics courses': physics_courses,
    'Electrical engineering': electrical_engineering_courses,
    'Computer science': computer_science_courses,
    'Civial and environmental engineering': civil_and_environmental_engineering_courses
}
# Create student objects
student1 = Student("Alice", "Chemical Engineering", "12345")
student2 = Student("Bob", "Computer and Electrical Engineering", "54321")
student3 = Student("Charlie", "Civil and Environmental Engineering", "67890")
student4 = Student("David", "Computer Science", "13579")
student5 = Student("Eve", "Electrical Engineering", "24680")
student6 = Student("Frank", "Physics", "98765")


# Add time slots for courses
for course in chemical_engineering_courses + computer_and_electrical_engineering_courses+physics_courses+electrical_engineering_courses+computer_science_courses+civil_and_environmental_engineering_courses+all_elective_courses:
    if course.credits == 4:
        course.add_time_slots(
            ("Monday", "9:00", "12:00"),
            ("Wednesday", "9:00", "12:00")
        )
    elif course.credits == 1:
        course.add_time_slots(
            ("Friday", "14:00", "15:00"),
            ("Thursday", "10:00", "11:00")
        )
# students list
students = [student1, student2, student3, student4, student5, student6]


# Function to check if a student has completed the prerequisites for a course
def has_prerequisites(student, course_code):
    course = next((c for courses in all_major_courses.values() for c in courses if c.code == course_code), None)
    if not course:
        return False  # Course not found
    if not course.prerequisites:
        return True  # Course has no prerequisites

    return course.prerequisites in student.completed_courses
# Function to load student info from the csv file
def load_student_info():
    students = []
    try:
        with open('student_info.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                name, student_id, major, completed_courses_str, registered_courses_str = row
                completed_courses = completed_courses_str.split(', ')
                registered_courses = {}
                if registered_courses_str:
                    for course_info in registered_courses_str.split(', '):
                        course, time_slot = course_info.split(' (')
                        time_slot = time_slot[:-1]  # Remove trailing ')'
                        registered_courses[course] = time_slot
                student = Student(name, student_id, major)
                student.completed_courses = completed_courses
                student.schedule = registered_courses
                students.append(student)
    except FileNotFoundError:
        pass  # File not found, return an empty list of students
    return students
# Function to save student information and registered courses to a CSV file
def save_student_info():
    with open('student_info.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Student ID', 'Major', 'Completed Courses', 'Registered Courses'])
        for student in students:
            writer.writerow([student.name, student.student_id, student.major, ', '.join(course.code for course in student.completed_courses), ', '.join([f"{course.code} ({time_slot[0]}: {time_slot[1]} - {time_slot[2]})" for course, time_slot in student.schedule.items()])])


# Input student name and ID
input_name = input("Please enter your name: ")
input_id = input("Please enter your student ID: ")

# Find the student object with matching name and ID
student = next((s for s in students if s.name == input_name and s.student_id == input_id), None)

if student is None:
    print("Student not found.")
else:
    print("\n=== Course Registration System ===")
    print(f"Welcome, {student.name}!")
    print(student)
    print("Available Actions:")
    print("1. Enroll in a course")
    print("2. Drop a course")
    print('3. Add a nwe student')
    print('4. Quit')

    action = input("Enter the number of the action you want to perform (or 'q' to quit): ")

    while action == '1':
        print("Available Courses:")
        if student.get_total_credits() < 18:
            print("Major Courses:")
            for course in all_major_courses.get(student.major, []):
                print(course)
                print("Time Slots:")
                for time_slot in course.time_slots:
                    print(f"{time_slot[0]}: {time_slot[1]} - {time_slot[2]}")

            print("Elective Courses:")
            for course in all_elective_courses:
                print(course)
                print("Time Slots:")
                for time_slot in course.time_slots:
                    print(f"{time_slot[0]}: {time_slot[1]} - {time_slot[2]}")

        else:
            print("Maximum credit limit reached.")
        break
    while action != 'q':
        if action == '1':
            if student.get_total_credits() < 18:
                chosen_course_code = input("Enter the course code you want to enroll in (or 'q' to quit): ")
                if chosen_course_code.lower() == 'q':
                    break
                chosen_course = next(
                    (course for course in all_major_courses.get(student.major, []) + all_elective_courses if
                     course.code == chosen_course_code), None)
                if not chosen_course:
                    print("Course not found. Please enter a valid course code.")
                    continue

                if chosen_course in all_major_courses.get(student.major, []) and not has_prerequisites(student, chosen_course_code):
                    print("Prerequisites not met.")
                    continue

                print("Available Time Slots:")
                for i, time_slot in enumerate(chosen_course.time_slots, 1):
                    print(f"{i}: {time_slot[0]}: {time_slot[1]} - {time_slot[2]}")

                chosen_time_slot_index = input("Enter the number of the time slot you want to choose: ")
                try:
                    chosen_time_slot_index = int(chosen_time_slot_index) - 1
                    if 0 <= chosen_time_slot_index < len(chosen_course.time_slots):
                        time_slot = chosen_course.time_slots[chosen_time_slot_index]
                        student.register_course(chosen_course, time_slot)
                        print(f"Total credits: {student.get_total_credits()}")
                        if student.get_total_credits() >= 16:
                            print("Minimum credit requirement met.")
                        if student.get_total_credits() > 18:
                            print("Maximum credit limit exceeded. Please drop a course.")
                    else:
                        print("Invalid time slot number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                print("Maximum credit limit reached.")

        elif action == '2':
            print("Registered Courses:")
            for course, time_slot in student.schedule.items():
                print(f"{course} ({time_slot})")

            drop_course_code = input("Enter the course code you want to drop (or 'q' to quit): ")
            if drop_course_code.lower() == "q":
                break

            drop_course = next((course for course in student.courses if course.code == drop_course_code), None)
            if not drop_course:
                print("Course not found. Please enter a valid course code.")
                continue

            student.drop_course(drop_course)
            print(f"Total credits: {student.get_total_credits()}")

        # action = input("Enter the number of the action you want to perform (or 'q' to quit): ")

        elif action == '3':
            # Add new student
            name = input("Enter the new student's name: ")
            student_id = input("Enter the new student's ID: ")
            major = input("Enter the new student's major: ")
            new_student = Student(name, major, student_id)
            students.append(new_student)
            print(f"New student {name} added.")
        elif action == '4':
        # Quit program
            break
        else:
            print("Invalid action. Please try again.")
        action = input("Enter the number of the action you want to perform (or 'q' to quit): ")
save_student_info()
print("Student information saved to 'student_info.csv'")
print(f"{student.name} registered courses:")
for course, time_slot in student.schedule.items():
    print(f"{course} ({time_slot})")
