class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def __str__(self):  # method overriding, called by default when called the obj
        return f"Name: {self.name}, Balance: {self.balance}"

    def __add__(self, other):  # operater overloading, based on operands u pass
        return Account("combined", self.balance + other.balance)

    def __gt__(self, other):  # operater overloading
        return self.balance > other.balance


user1 = Account("manjot", 10000)
user2 = Account("charan", 20000)
user3 = Account("dheer", 40000)

print(user1)
print(user2)
print(user3)
print(user1 + user2 + user3)

print(user1 < user2 < user3)
print(user1 > user2 > user3)
