class Computer:

    brand = "LENOVO"  # class variable

    def __init__(self, cpu, ram, ssd):
        self.cpu = cpu  # instance variable
        self.ram = ram
        self.ssd = ssd

    def get_config(self):  # instance method,  to interact with class objs
        print(f"config: {self.brand}, {self.cpu}, {self.ram}, {self.ssd}")

    @classmethod
    def get_brand_name(cls):  # class method, to intract with class variable
        return cls.brand

    @staticmethod
    def gb_to_bytes(gb):  # static method , for utility
        return gb * (1024**3)


com1 = Computer(cpu="i3", ram="4GB", ssd="512GB")

com1.get_config()
print(com1.get_brand_name())
print(com1.gb_to_bytes(16))
print(Computer.get_brand_name())  # can be called with class no need of obj creation
print(Computer.gb_to_bytes(16))  # can be called with class no need of obj creation
