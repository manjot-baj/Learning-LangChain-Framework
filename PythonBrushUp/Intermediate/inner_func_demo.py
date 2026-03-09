def outer():
    print("IM OUTER")

    def inner():
        print("IM INNER")

    return inner


myInner = outer()
print(myInner())
