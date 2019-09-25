from valerymain import Valery
from threading import Event
import threading
import time


valery = Valery.Valery()


def main():
    valery.quick_start()
    time.sleep(1000000)


if __name__ == "__main__":
    main()


