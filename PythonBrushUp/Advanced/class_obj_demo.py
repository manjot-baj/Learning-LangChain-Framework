class computer:

    name = "LENOVO"  # class variable , shared by every object

    def __init__(
        self, cpu, ram, ssd
    ):  # Called in every object creation, but not a constructor
        self.cpu = cpu  # instance variable , specific to instance object
        self.ram = ram
        self.ssd = ssd

    def get_config(self):
        print(f"config: {self.name}, {self.cpu}, {self.ram}, {self.ssd}")


com1 = computer(cpu="i3", ram="4GB", ssd="512GB")
com2 = computer(cpu="i9", ram="32GB", ssd="2TB")
com1.get_config()
com2.get_config()
