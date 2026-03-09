from threading import Thread
from time import sleep


# -----Class approch----------
class Hello(Thread):
    def run(self):
        for i in range(5):
            print("Hello", i + 1)
            sleep(0.2)


class Hi(Thread):
    def run(self):
        for i in range(5):
            print("Hi", i + 1)
            sleep(0.2)


# -----functional approch----------
def hello():
    for i in range(5):
        print("Hello", i + 1)
        sleep(0.2)


def hi():
    for i in range(5):
        print("Hi", i + 1)
        sleep(0.2)


if __name__ == "__main__":
    # t1 = Hello()
    # t2 = Hi()

    t1 = Thread(target=hello)
    t2 = Thread(target=hi)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Bye")
