print(10 > 9)  # True
print(10 == 9) # False
print(10 < 9) # False

print(5 >= 5) # True
print(5 <= 5) # True
print(5 != 5) # False 



print(bool("Hello")) # True
print(bool(15))      # True
print(bool(""))     # False
print(bool(0))      # False
print(bool(None))   # False
print(bool([]))     # False
print(bool({}))     # False
print(bool(()))     # False



class myclass():
  def __len__(self):
    return 0
myobj = myclass()
print(bool(myobj)) # False