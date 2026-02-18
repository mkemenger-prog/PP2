class Father:
    def skills(self):
        print("Father: driving")

class Mother:
    def skills(self):
        print("Mother: cooking")

class Child(Father, Mother):
    pass

c = Child()
c.skills()



class Math:
    def add(self, a, b):
        return a + b

class Science:
    def subject(self):
        return "Physics"

class Student(Math, Science):
    pass

s = Student()
print(s.add(2, 3))      # 5
print(s.subject())      # Physics


class A:
    def show(self):
        print("A")

class B:
    def show(self):
        print("B")

class C(A, B):
    def show(self):
        super().show()
        print("C")

c = C()
c.show()

