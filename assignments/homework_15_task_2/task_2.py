class Dog:

    age_factor = 7

    def __init__(self, dogs_age):
        self.dogs_age = dogs_age

    def human_age(self):
        return print(f"{self.dogs_age * Dog.age_factor} years old")

dogs_human_age = Dog(3)

dogs_human_age.human_age()