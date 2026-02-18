students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)
# Output: [('Tobias', 22), ('Emil', 25), ('Linus', 28)]


students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
sorted_students = sorted(students, key=lambda x: x[1], reverse=True)
print(sorted_students)
# Output: [('Bob', 92), ('Alice', 85), ('Charlie', 78)]

words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)
# Output: ['pie', 'apple', 'banana', 'cherry']