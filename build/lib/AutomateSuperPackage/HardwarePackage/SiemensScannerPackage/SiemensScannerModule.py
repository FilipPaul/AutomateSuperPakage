import hid
class SiemensScannerClass:
    def __init__(self):
        print("Hello Im HWellScanner Class")
    
    class HIDcommunication:
        def __init__(self, VENDOR_ID ,PRODUCT_ID):
            self.VENDOR_ID = VENDOR_ID
            self.PRODUCT_ID = PRODUCT_ID
            self.device = hid.device()

        def setCOM(self):
            if len(hid.enumerate(self.VENDOR_ID, self.PRODUCT_ID)) > 0:
                print(hid.enumerate(self.VENDOR_ID, self.PRODUCT_ID))
                self.device.open(self.VENDOR_ID, self.PRODUCT_ID)
                return 1
            else:
                print("DEVICE not found")
                return 0
        
        def reset_input_buffer(self):
            while True:
                data = self.device.read(300,1)
                if data:
                    ...
                else:
                    break
    
        def selfCheck(self):
            if len(hid.enumerate(self.VENDOR_ID, self.PRODUCT_ID)) > 0:
                return 1
            else:
                return 0

        def NonBlockingRead(self):
            data = self.device.read(300,1)
            if data:
                output = ""
                for d in data:
                    output += chr(d)
                pos = output.encode("utf").find(b"\x01X\x1ean//n\x04")
                if pos > -1:
                    output = output[:pos]
                print(output)
                return [True, output + "\r"]
            else:
                return [False, "empty"]

                