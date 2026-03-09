def add(num1=0, num2=0):  # default argument
    return num1 + num2


def add(num1, *num2):  # variable length arguments
    sum = num1
    for n in num2:
        sum += n
    return sum


result = add(4, 5)
result = add(4)
result = add(2, 3, 4, 5, 1, 3, 4, 4, 33)

print(result)


def person(name, age):
    return f"Name: {name}, Age: {age}"


print(person(name="Manjot", age=28))  # Keyword arguments


def person(name, **kwargs):
    print(f"Name: {name}")
    for k, v in kwargs.items():
        print(f"{k}: {v}")


person(
    name="Manjot", age=28, location="Mumbai", tech="Python"
)  # variable length Keyword arguments
