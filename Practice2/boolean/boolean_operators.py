x = 5

print(x > 3 and x < 10)   # True


x = 2

print(x > 5 or x < 3)    # True

x = 5

print(not x > 3)        # False


age = 18

print(age >= 18 and age < 65)

is_adult = age >= 18
has_ticket = True
can_enter = is_adult and has_ticket
print(can_enter)  # True

is_weekend = False
is_holiday = True
can_relax = is_weekend or is_holiday
print(can_relax)  # True