import os
import json
class Person:
    """
    Base class representing a generic Person.
    Demonstrates Inheritance.
    """
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
    def display_info(self):
        """Placeholder method to be overridden (Polymorphism)"""
        pass
class Student(Person):
    """
    Student class inherits from Person.
    Manages specific student details like marks and grades.
    """
    def __init__(self, name, student_id, marks):
        super().__init__(name, student_id)
        self.__marks = marks  
        self.grade = self.calculate_grade()
    def calculate_grade(self):
        """Calculates grade based on marks."""
        if self.__marks >= 90: return 'A'
        elif self.__marks >= 80: return 'B'
        elif self.__marks >= 70: return 'C'
        elif self.__marks >= 60: return 'D'
        else: return 'F'
    def get_marks(self):
        return self.__marks
    def set_marks(self, new_marks):
        if 0 <= new_marks <= 100:
            self.__marks = new_marks
            self.grade = self.calculate_grade() 
        else:
            print("❌ Invalid marks! Range must be 0-100.")
    def display_info(self):
        return f"ID: {self.student_id} | Name: {self.name} | Marks: {self.__marks} | Grade: {self.grade}"
    def to_dict(self):
        return {
            "name": self.name,
            "student_id": self.student_id,
            "marks": self.__marks
        }
class StudentManager:
    """
    Manages the list of students and File I/O operations.
    """
    def __init__(self):
        self.students = []
        self.filename = "students.json"
        self.load_data()
    def load_data(self):
        """Loads data from JSON file on startup."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    for entry in data:
                        student = Student(entry['name'], entry['student_id'], entry['marks'])
                        self.students.append(student)
            except Exception as e:
                print(f"⚠️ Error loading file: {e}")
        else:
            with open(self.filename, 'w') as file:
                json.dump([], file)
    def save_data(self):
        """Saves current list of students to JSON file."""
        try:
            with open(self.filename, 'w') as file:
                data = [s.to_dict() for s in self.students]
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    def add_student(self):
        try:
            s_id = input("Enter Student ID: ").strip()
            if any(s.student_id == s_id for s in self.students):
                print("❌ Student ID already exists!")
                return
            name = input("Enter Name: ").strip()
            marks = float(input("Enter Marks (0-100): "))
            if 0 <= marks <= 100:
                new_student = Student(name, s_id, marks)
                self.students.append(new_student)
                self.save_data()
                print("✅ Student added successfully!")
            else:
                print("❌ Marks must be between 0 and 100.")
        except ValueError:
            print("❌ Invalid input! Please enter numbers for marks.")
    def view_students(self):
        print("\n--- 📋 Student Records ---")
        if not self.students:
            print("No records found.")
        else:
            for student in self.students:
                print(student.display_info())
        print("--------------------------")
    def search_student(self):
        s_id = input("Enter Student ID to Search: ").strip()
        found = False
        for student in self.students:
            if student.student_id == s_id:
                print("\n✅ Record Found:")
                print(student.display_info())
                found = True
                break
        if not found:
            print("❌ Student not found.")
    def update_student(self):
        s_id = input("Enter Student ID to Update: ").strip()
        for student in self.students:
            if student.student_id == s_id:
                print(f"Current Data: {student.display_info()}")
                try:
                    new_name = input("Enter New Name (Press Enter to keep current): ")
                    new_marks_str = input("Enter New Marks (Press Enter to keep current): ")
                    if new_name:
                        student.name = new_name
                    if new_marks_str:
                        student.set_marks(float(new_marks_str))
                    self.save_data()
                    print("✅ Record updated successfully!")
                    return
                except ValueError:
                    print("❌ Invalid marks entered.")
                    return
        print("❌ Student ID not found.")
    def delete_student(self):
        s_id = input("Enter Student ID to Delete: ").strip()
        for student in self.students:
            if student.student_id == s_id:
                self.students.remove(student)
                self.save_data()
                print("✅ Student deleted successfully!")
                return
        print("❌ Student ID not found.")
def main():
    system = StudentManager()
    while True:
        print("\n🎓 === SMART STUDENT MANAGEMENT SYSTEM === 🎓")
        print("1. Add New Student")
        print("2. Display All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        choice = input("👉 Enter your choice (1-6): ")
        if choice == '1':
            system.add_student()
        elif choice == '2':
            system.view_students()
        elif choice == '3':
            system.search_student()
        elif choice == '4':
            system.update_student()
        elif choice == '5':
            system.delete_student()
        elif choice == '6':
            print("👋 Exiting... Data saved. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please select 1-6.")
if __name__ == "__main__":
    main()