import re

pattern = r"ab*"

tests = ["a", "ab", "abbb", "ac"]
for t in tests:
    print(t, "->", bool(re.fullmatch(pattern, t)))



import re

pattern = r"ab{2,3}"

tests = ["abb", "abbb", "abbbb", "ab"]
for t in tests:
    print(t, "->", bool(re.fullmatch(pattern, t)))



import re

pattern = r"[a-z]+(_[a-z]+)+"

text = "hello_world test_123 abc_def_ghi"
print(re.findall(pattern, text))




import re

pattern = r"[A-Z][a-z]+"

text = "Hello world Test ABC"
print(re.findall(pattern, text))




import re

pattern = r"a.*b"

tests = ["ab", "axxxb", "acb", "a123b"]
for t in tests:
    print(t, "->", bool(re.fullmatch(pattern, t)))






import re

text = "Hello, world. Python is fun"
result = re.sub(r"[ ,\.]", ":", text)
print(result)





import re

def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)

print(snake_to_camel("hello_world_test"))




import re

text = "HelloWorldPython"
result = re.split(r"(?=[A-Z])", text)
print(result)





import re

text = "HelloWorldPython"
result = re.sub(r"(?<!^)(?=[A-Z])", " ", text)
print(result)






import re

def camel_to_snake(text):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()

print(camel_to_snake("HelloWorldPython"))


