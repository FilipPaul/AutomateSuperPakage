import serial.tools.list_ports
import serial

#GWINSTEK PSU 
class GwinstekGPD2323Class:
    def __init__(self):
        print("Hello Im GWINSTEK Class")
    
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
            

        def InfoCommand(self,Command):
            self.Write(Command)
            packet = self.ComInstance.read_until("\n".encode('utf-8'), 600)
            #print(packet)
            packet = packet.decode('utf-8')
            #print(packet)
            if -1 == packet.find("\n"):
                print("ERROR calling command: " + Command + "\n")
                return [0,packet]
            #­self.ComInstance.close()
            #print("OK")
            return [1,packet]
        
        def SetCommand(self,Command):
            self.Write(Command)