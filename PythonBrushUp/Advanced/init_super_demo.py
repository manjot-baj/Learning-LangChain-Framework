# In python, By default each class inherits "object class" so every class is a child class


class A:  # Parent/Super/Base class

    def __init__(self):
        print("A init called")

    def f1(self):
        print("F1 works")


class B(A):  # Child/Sub/Derived class

    def __init__(self):
        super().__init__()  # to call the init method from parent
        print("B init called")

    def f2(self):
        super().f1()  #  way 1: to call the other method from parent
        self.f1()  # way 2:  to call the other method from parent
        print("F2 works")


obj2 = B()
obj2.f2()
