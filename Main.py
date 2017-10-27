from Controller import *
import ctypes

def main():
    #caseID = "loan"
    caseID = "contract"

    #strategy = "random"
    strategy = "exhaustive"

    user32 = ctypes.windll.user32
    simulation = Controller(user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 200, caseID)
    simulation.run()

if __name__ == '__main__':
    main()

