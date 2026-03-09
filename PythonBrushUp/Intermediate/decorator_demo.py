def greater_first(func):
    def wrapper(a, b):
        a, b = b, a
        return func(a, b)

    return wrapper


def log_deco(func):
    def wrapper(*args, **kwargs):
        print(f"values {args} {kwargs}")
        ret = func(*args, **kwargs)
        print(f"Result {ret}")
        return func(*args, **kwargs)

    return wrapper


@log_deco
@greater_first
def sub(a, b):
    return a - b


@greater_first
def divide(a, b):
    return a / b


print(sub(2, 4))
print(divide(2, 4))
