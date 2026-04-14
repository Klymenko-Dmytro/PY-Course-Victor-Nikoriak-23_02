class Animal:
    def talk(self):
        pass

class Dog(Animal):
    def talk(self):
        print("woof! woof! woof!")

class Cat(Animal):
    def talk(self):
        print("meow! meow! meow!")

c = Cat()
d = Dog()

def say_animals(x):
    return x.talk()


say_animals(c)
say_animals(d)