from Controller import *
import ctypes
from YamlReader import *


def main():

    user32 = ctypes.windll.user32
    simulation = Controller(user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 200)
    simulation.run()

    #yaml = YamlReader("./Cases/debt.yaml")

if __name__ == '__main__':
    main()

