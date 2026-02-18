class Animal:
    def speak(self):
        print("The animal makes a sound")

class Dog(Animal):
    def speak(self):
        print("The dog barks")

a = Animal()
d = Dog()

a.speak()  # The animal makes a sound
d.speak()  # The dog barks



class Vehicle:
    def move(self):
        print("The vehicle moves")

class Car(Vehicle):
    def move(self):
        super().move()
        print("The car drives on roads")

c = Car()
c.move()



class Calculator:
    def calculate(self, x, y):
        return x + y

class AdvancedCalculator(Calculator):
    def calculate(self, x, y):
        return x * y

calc = Calculator()
adv = AdvancedCalculator()

print(calc.calculate(3, 4))   # 7
print(adv.calculate(3, 4))    # 12
