#from serial.serialwin32 import Serial
import serial.tools.list_ports
import serial
import os



class ArigoClass:
    def __init__(self):
        print("Hello Im FlashRunner Class")
    
    class SerialCommunication:
        ComInstance = serial.Serial()
        def __init__(self):
            print("Hello im SerialCommunication Class based on serial.Serial()")

        def Write(self,Command):
            UpdateString = Command + "*"
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

            packet = self.ComInstance.read_until("\n".encode('utf-8'), 600)
            if -1 == packet.find("System ready\r".encode('utf-8')):
                print("ERROR calling command: Open PORT")
                return 0
            else:
                return 1
            #print("OK")
            

        def NormalCommand(self,Command):
            self.Write(Command)
            packet = self.ComInstance.read_until("*".encode('utf-8'), 600)
            #print(packet)
            packet = packet.decode('utf-8')
            #print(packet)
            if -1 == packet.find("ACK*"):
                print("ERROR calling command: " + Command + "*")
                return [0,packet]
            #­self.ComInstance.close()
            #print("OK")
            return [1,packet]
            
