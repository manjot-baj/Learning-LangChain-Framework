class Laptop:  # Duck
    def build(self):  # Quacking
        print("Laptop Building....")


class Desktop:  # Not a Duck
    def build(self):  # But Quacking
        print("Desktop Building....")


class Tablet:  # Not a Duck
    def read_pdf(self):  # And Not Quacking
        print("Tablet Reading....")


class Coder:
    def code(self, machine: Laptop):  # Expecting Duck to Quack
        print("Coder is coding ....")
        machine.build()


lenovo_ideapad = Laptop()
acer_boost = Desktop()
apple_tab = Tablet()
manjot = Coder()

manjot.code(lenovo_ideapad)
manjot.code(acer_boost)  # shows duck type polymorphism
manjot.code(apple_tab)  ## error as this method is not available with our duck
