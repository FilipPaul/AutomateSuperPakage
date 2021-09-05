import serial.tools.list_ports
import serial

class HWellScannerClass:
    def __init__(self):
        print("Hello Im HWellScanner Class")
    
    class SerialCommunication:
        ComInstance = serial.Serial()
        def __init__(self):
            print("Hello im SerialCommunication Class based on serial.Serial()")

        def Write(self,Command):
            UpdateString = Command + "\n"
            #print(UpdateString)
            self.ComInstance.write(UpdateString.encode('utf-8'))

        def setCOM(self,COMobject):
            self.ComInstance.baudrate = COMobject.baudrate
            self.ComInstance.port = COMobject.port
            self.ComInstance.timeout = COMobject.timeout
            self.ComInstance.parity = COMobject.parity
            self.ComInstance.stopbits = COMobject.stopbits
            self.ComInstance.bytesize = COMobject.bytesize
            try:
                self.ComInstance.open()
            except:
                self.ComInstance.close()
                self.ComInstance.open()

        def Read(self):
            while True:
                bytesToRead = self.ComInstance.in_waiting
                if(bytesToRead > 0):
                    packet = self.ComInstance.read_until("\r".encode('utf-8'), 600)
                    self.ComInstance.reset_input_buffer()
                    packet = packet.decode('utf-8')
                    #print(packet)
                    if -1 == packet.find("\r"):
                        print("ERROR Reading Barcode\n")
                        return [0,packet]
                    #­self.ComInstance.close()
                    #print("OK")
                    return [1,packet]
                    