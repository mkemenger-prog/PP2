numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)
# Output: [1, 3, 5, 7]

numbers = [10, 15, 20, 25, 30]
result = list(filter(lambda x: x > 20, numbers))
print(result)
# Output: [25, 30]

numbers = [1, 2, 3, 4, 5, 6]
result = list(filter(lambda x: x % 2 == 0, numbers))
print(result)
# Output: [2, 4, 6]