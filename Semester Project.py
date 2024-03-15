class College:
    def __init__(self, name, majors):
        self.name = name
        self.majors = majors

class Major:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses

class Course:
    def __init__(self, name, prerequisites=None):
        self.name = name
        self.prerequisites = prerequisites if prerequisites else []

class Student:
    def __init__(self, name, college, major):
        self.name = name
        self.college = college
        self.major = major
        self.courses_taken = []

    def enroll(self, course):
        if course in self.courses_taken:
            print(f"{self.name} is already enrolled in {course.name}.")
        else:
            prerequisites_met = all(prerequisite in self.courses_taken for prerequisite in course.prerequisites)
            if prerequisites_met:
                self.courses_taken.append(course)
                print(f"{self.name} has successfully enrolled in {course.name}.")
            else:
                print(f"{self.name} does not meet the prerequisites for {course.name}.")

    def drop(self, course):
        if course in self.courses_taken:
            self.courses_taken.remove(course)
            print(f"{self.name} has dropped {course.name}.")
        else:
            print(f"{self.name} is not enrolled in {course.name}.")

