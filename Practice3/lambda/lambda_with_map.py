numbers = [1, 2, 3, 4, 5]

result = list(map(lambda x: x + 10, numbers))
print(result)
# Output: [11, 12, 13, 14, 15]


numbers = [1, 2, 3, 4]

result = list(map(lambda x: x * 3, numbers))
print(result)
# Output: [3, 6, 9, 12]


numbers = [2, 3, 4, 5]

result = list(map(lambda x: x ** 2, numbers))
print(result)
# Output: [4, 9, 16, 25]



numbers = [-5, -2, 0, 3, -7]

result = list(map(lambda x: abs(x), numbers))
print(result)
# Output: [5, 2, 0, 3, 7]


