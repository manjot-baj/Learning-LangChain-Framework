def add(a, b):
    return a + b


# __name__ value is __main__
# if we execute the same file with function for results
# else the value is the file name or module name 
# when we use the functions or anything in any other file and execite

if __name__ == "__main__":
    print(add(1, 2))
