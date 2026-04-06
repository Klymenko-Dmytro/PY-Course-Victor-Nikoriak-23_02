class Pesrson:
    def __init__(self, first_name, last_name, age, gender, number_school):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.number_school = number_school

    def hello(self):
        return print(f'Hello! I am {self.first_name} {self.last_name}! I {self.age} years old.')


class Teacher(Pesrson):
    status = "teacher"
    def __init__(self, first_name, last_name, age, gender, number_school, salary):
        super().__init__(first_name, last_name, age, gender, number_school)
        self.salary = salary

    def greeting(self):
        return print(f'i am a {Teacher.status}. I work at school number {self.number_school} and my salary: {self.salary}')

class Student(Pesrson):
    status = "student"
    def __init__(self, first_name, last_name, age, gender, number_school, number_class):
        super().__init__(first_name, last_name, age, gender, number_school)
        self.number_class = number_class

    def greeting(self):
        return print(f'I am a {Student.status}, study at {self.number_class} group in school number: {self.number_school}')


t = Teacher("Ivanov", "Ivan","30","m","54", "10000")
s = Student('Smyrnov', "Sergiy","15","m","54", "10-B")
t.hello()
t.greeting()
s.hello()
s.greeting()

