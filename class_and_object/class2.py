class Person:
    counter = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Person.counter += 1

    def greet(self):
        return f"Hi, it's {self.name}."
    

p1 = Person('Alex', 28)
p2 = Person('Kebe', 22)
p3 = Person('abbe',44)
print(Person.counter)