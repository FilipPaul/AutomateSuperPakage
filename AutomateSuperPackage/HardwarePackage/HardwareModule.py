from AutomateSuperPackage.HardwarePackage.FlashRunnerPackage.FlashRunnerModule import FlashRunnerClass
from AutomateSuperPackage.HardwarePackage.ArigoPackage.ArigoModule import ArigoClass
class HardwareClass:
    def __init__(self):
        print("IM HARDWARE CLASS")
        self.FlashRunner = FlashRunnerClass()
        self.Arigo = ArigoClass()
