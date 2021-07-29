#from serial.serialwin32 import Serial
import serial.tools.list_ports
import serial
#from YModem import YModem
import os
from AutomateSuperPackage.HardwarePackage.FlashRunnerPackage.YModem import YModem
#This packages is based on this package: (I did only minor changes to suit it up to my project..)
#https://github.com/tehmaze-labs/modem/tree/multi-protocol

class FlashRunnerClass:
    def __init__(self):
        print("Hello Im FlashRunner Class")
        

    class SerialCommunication:
        ComInstance = serial.Serial()
        def __init__(self):
            print("Hello im SerialCommunication Class based on serial.Serial()")
        

        def OpenAndWrite(self,Command):
            print(Command)
            try:
                self.ComInstance.close()
            except:
                print("Was Already closed")
            self.ComInstance.open()
            UpdateString = Command + "\r"
            self.ComInstance.write(UpdateString.encode('utf-8'))

        def setCOM(self,COMobject):
            self.ComInstance.baudrate = COMobject.baudrate
            self.ComInstance.port = COMobject.port
            self.ComInstance.timeout = COMobject.timeout
            self.ComInstance.parity = COMobject.parity
            self.ComInstance.stopbits = COMobject.stopbits
            self.ComInstance.bytesize = COMobject.bytesize

        def NormalCommand(self,Command):
            self.OpenAndWrite(Command)
            packet = self.ComInstance.read_until("\r".encode('utf-8'), 600)
            packet = packet.decode('utf-8')
            print(packet)
            if -1 == packet.find(">"):
                print("ERROR calling command: " + Command)
                #exit()
                return 0
            self.ComInstance.close()
            return 1
            
        def sender_getc(self,size):
            return self.ComInstance.read(size) or None

        def sender_putc(self,data, timeout=10):
            return self.ComInstance.write(data)



        def SendFileToCommand(self,Command,filename):
            self.OpenAndWrite(Command)
            sender = YModem(self.sender_getc, self.sender_putc)
            #os.chdir(sys.path[0])
            file_path = os.path.abspath(filename)
            sender.send_file(file_path)
            self.ComInstance.close()


        def receiver_getc(self,size):
                return self.ComInstance.read(size) or None

        def receiver_putc(self,data, timeout=10):
            return self.ComInstance.write(data)


        def GetFileFromCommand(self,Command,outputfile):
            self.OpenAndWrite(Command)
            receiver = YModem(self.receiver_getc, self.receiver_putc)
            #os.chdir(sys.path[0])
            #root_path = os.path.abspath(outputfile)
            receiver.recv_file(outputfile)
            self.ComInstance.close()
