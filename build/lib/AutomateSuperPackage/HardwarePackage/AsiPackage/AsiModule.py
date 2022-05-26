import serial.tools.list_ports
import serial

#ASI MODULE
class AsiClass:
    def __init__(self):
        print("Hello Im ASI Class")
    
    class SerialCommunication:
        ComInstance = serial.Serial()
        def __init__(self):
            print("Hello im SerialCommunication Class based on serial.Serial()")

        def Write(self,Command):
            try:
                self.ComInstance.close()
            except:
                print("Was Already closed")
            self.ComInstance.open()
            UpdateString = Command + "\r"
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
                    
        def NormalCommand(self,Command):
            self.Write(Command)

            packet = self.ComInstance.read_until("\r".encode('utf-8'), 0xFFFFFFF)
            #print(packet)
            #with open("Log.txt","a") as file:
            #    file.write("COMMAND: "+ Command + " --> : RESPONSE: " + packet)
            #    file.close()
            #if -1 == packet.find(">"):
            #    print("ERROR calling command: " + Command)
                #exit()
            #    return 0,packet
            self.ComInstance.close()
            return 1,str(packet)