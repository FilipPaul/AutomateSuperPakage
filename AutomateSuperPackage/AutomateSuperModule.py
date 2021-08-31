from AutomateSuperPackage.HardwarePackage.HardwareModule import HardwareClass
from AutomateSuperPackage.DatabasePackage.DatabaseModule import DatabaseClass

class SuperClass:
    def __init__(self):
        self.database = DatabaseClass()
        self.Hardware = HardwareClass()

    def printfun(self):
        print(self)

