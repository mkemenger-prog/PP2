class Person:
  def __init__(self, name):
    self.name = name

  def greet(self):
    print("Hello, my name is " + self.name) # Output: Hello, my name is Emil

p1 = Person("Emil")
p1.greet()



class Calculator:
  def add(self, a, b):
    return a + b

  def multiply(self, a, b):
    return a * b

calc = Calculator()
print(calc.add(5, 3))# Output: 8``
print(calc.multiply(4, 7))# Output: 28

