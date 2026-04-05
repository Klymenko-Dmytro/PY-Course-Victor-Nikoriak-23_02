class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def talk(self):
        return print(f"Hello, my name is {self.first_name} {self.last_name} and I’m {self.age} years old!")


greeting = Person("Dmytro", "Klymenko", 38)

greeting.talk()