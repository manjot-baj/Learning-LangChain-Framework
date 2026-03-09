def square(num):
    return num * num


def cube(num):
    return num * num * num


def perform_operation(
    num, operation
):  # Higher Order Function, (Function is passed as args for function)
    return operation(num)


print(perform_operation(34, square))
