class Person:
    def __init__(self, name, age=27):
        self.name = name
        self.age = age


if __name__ == '__main__':
    p= Person('Alex')
    print(f"I'm {p.name}. I'm {p.age} years old.")
