from abc import ABC, abstractmethod


class PaymentGateway(ABC):  # abstract class, obj cannot be created of abstract class

    @abstractmethod
    def pay(self):  # abstract method
        pass


class BharatPay(PaymentGateway):

    def pay(self):
        print("Paying with BharatPay....")


class PhonePay(PaymentGateway):

    def pay(self):
        print("Paying with PhonePay....")


class Purchase:
    def __init__(self, gateway):
        self.gateway = gateway

    def checkout(self):
        print("Purchasing begin...")
        self.gateway.pay()


gateway1 = BharatPay()
gateway2 = PhonePay()
purchase1 = Purchase(gateway1)
purchase2 = Purchase(gateway2)

purchase1.checkout()
purchase2.checkout()
