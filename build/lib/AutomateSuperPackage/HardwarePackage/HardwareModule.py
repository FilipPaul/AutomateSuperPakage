from AutomateSuperPackage.HardwarePackage.FlashRunnerPackage.FlashRunnerModule import FlashRunnerClass
from AutomateSuperPackage.HardwarePackage.ArigoPackage.ArigoModule import ArigoClass
from AutomateSuperPackage.HardwarePackage.GwinstekGPD2323Package.GwinstekGPD2323Module import GwinstekGPD2323Class
from AutomateSuperPackage.HardwarePackage.HWellScannerPackage.HWellScannerModule import HWellScannerClass
from AutomateSuperPackage.HardwarePackage.AsiPackage.AsiModule import AsiClass
from AutomateSuperPackage.HardwarePackage.SiemensScannerPackage.SiemensScannerModule import SiemensScannerClass
class HardwareClass:
    def __init__(self):
        print("IM HARDWARE CLASS")
        self.FlashRunner = FlashRunnerClass()
        self.Arigo = ArigoClass()
        self.GwinstekGPD2323 = GwinstekGPD2323Class()
        self.HWellScanner = HWellScannerClass()
        self.ASI = AsiClass()
        self.SiemensScanner = SiemensScannerClass()
