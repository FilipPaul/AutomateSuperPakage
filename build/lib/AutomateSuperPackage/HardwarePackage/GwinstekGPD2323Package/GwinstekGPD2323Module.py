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
            self.current_command = ""
            self.current_response = ""

        def Write(self,Command):
            self.current_command = Command
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
            self.current_response = packet
            #print(packet)
            if -1 == packet.find("\n"):
                print("ERROR calling command: " + Command + "\n")
                self.current_response = "ERROR"
                return [0,packet]
            #­self.ComInstance.close()
            #print("OK")
            return [1,packet]
        
        def SetCommand(self,Command):
            self.Write(Command)
            