class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)
x = Student("Mike", "Olsen")
x.printname() #This will print "Mike Olsen" because the Student class inherits from the Person class, 
#and the super() function is used to call the __init__ method of the Person class to initialize the firstname and 
# #lastname attributes.


class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)
    self.graduationyear = 2019
x = Student("Mike", "Olsen")
print(x.graduationyear) #This will print "2019" because the graduationyear

