class A:  # Parent class
    def f1(self):
        print("F1 works")

    def f2(self):
        print("F2 works")


class B(A):  # Child class for A and Parent for C, Single level Inheritance
    def f3(self):
        print("F3 works")

    def f4(self):
        print("F4 works")


class C(B):  # Child class for B, Multi level Inheritance
    def f5(self):
        print("F5 works")

    def f6(self):
        print("F6 works")


class A1:
    def f1(self):
        print("F1 works")

    def f2(self):
        print("F2 works")

    def ff(self):
        print("Ff A works")


class B1:
    def f3(self):
        print("F3 works")

    def f4(self):
        print("F4 works")

    def ff(self):
        print("Ff B works")


class D(
    A1, B1
):  # Multiple Inheritance , MRO(Method Resolution order), if called the method is checked in own class, if not exists then in A first class/parent of inheritance and if not exists in that then to next class/parent B
    def f7(self):
        print("F7 works")


obj1 = A()
obj1.f1()
obj1.f2()

obj2 = B()
obj2.f1()
obj2.f2()
obj2.f3()
obj2.f4()

obj3 = C()
obj3.f1()
obj3.f2()
obj3.f3()
obj3.f4()
obj3.f5()
obj3.f6()

obj4 = D()
obj4.f1()
obj4.f2()
obj4.f3()
obj4.f4()
obj4.f7()
obj4.ff()

B1.ff(obj4)  # incase u want to purposely call the specific class method
