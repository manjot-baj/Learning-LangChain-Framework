class Abc:

    def __new__(cls):  # constrcutor , called behind the scene on object creation
        print("constructor called !!!")
        return super(Abc, cls).__new__(cls)

    def __init__(self):  # init, called behind the scene on object creation
        print("init Called !!!")

    def show(self):
        print("In Show !!!")


obj1 = Abc()  # ideal way to make class obj
obj1.show()

obj2 = Abc.__new__(Abc)  # works but not ideal
obj2.show()
