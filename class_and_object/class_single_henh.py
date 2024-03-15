from class3 import Person
class Employee(Person):
    def __init__(self, name, age, job_title):
        super().__init__(name, age)
        self.job_title = job_title

    def greet(self):
        return super().greet() + f" I'm a {self.job_title}."
    

employee = Employee('Alex', 25, 'Generative AI Engineer and Python Developer')
print(employee.greet())