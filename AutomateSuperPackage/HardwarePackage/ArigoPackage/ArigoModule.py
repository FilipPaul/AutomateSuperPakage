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
            except Exception:
                self.ComInstance.close()
                self.ComInstance.open()

            packet = self.ComInstance.read_until("\n".encode('utf-8'), 600)
            print("PACKET")
            if -1 == packet.find("System ready\r".encode('utf-8')):
                print("ERROR calling command: Open PORT")
                return 0,packet
            else:
                return 1,packet
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

        def GetIdPinStates(self,INPUT_PIN_0_LSB, INPUT_PIN_1, INPUT_PIN_2_MSB): #in form of string "IN_1", "IN_4", etc.. 
            [status,message] = self.NormalCommand("READPINS")
            if status == True:
                raw_ID_list = message.split(";")
                ID_POS_2_LSB = int(INPUT_PIN_0_LSB[-1:])
                ID_POS_1 = int(INPUT_PIN_1[-1:])
                ID_POS_0_MSB = int(INPUT_PIN_2_MSB[-1:])
                ID_of_adapter = raw_ID_list[ID_POS_0_MSB - 1] + raw_ID_list[ID_POS_1 - 1] + raw_ID_list[ID_POS_2_LSB - 1]
                return status,ID_of_adapter
        
        def GetNeedleinStates(self,connected_adapter,YAML): #in form of string "IN_1", "IN_4", etc.. 
            print("Needle state")
            [status,message] = self.NormalCommand("READPINS")
            if status == True:
                raw_ID_list = message.split(";")
                POS_A = int(YAML["ADAPTERS"][connected_adapter]["PINOUT"]["SWITCH_NEEDLE_A"][-1:])
                POS_B = int(YAML["ADAPTERS"][connected_adapter]["PINOUT"]["SWITCH_NEEDLE_B"][-1:])
                POS_C = int(YAML["ADAPTERS"][connected_adapter]["PINOUT"]["SWITCH_NEEDLE_C"][-1:])
                
                needle_state = [raw_ID_list[POS_A - 1], raw_ID_list[POS_B - 1] , raw_ID_list[POS_C - 1]]
                return status,needle_state

        def GetConnectedAdapter(self, YAML): #YAML is YAML config file
            find_adapter = ""
            all_adapters = []
            for i in range (0,YAML["ADAPTERS"]["TOTAL_NUMBER_OF_ADAPTERS"]):
                all_adapters.append("ADAPTER_" +  str(i+1) )
            for adapter in all_adapters:
                ID_2 = YAML["ADAPTERS"][adapter]["CONFIGURATION"]["PINOUT"]["ID_PIN_2"]
                ID_1 = YAML["ADAPTERS"][adapter]["CONFIGURATION"]["PINOUT"]["ID_PIN_1"]
                ID_0 = YAML["ADAPTERS"][adapter]["CONFIGURATION"]["PINOUT"]["ID_PIN_0"]
                [status, ID] = self.GetIdPinStates(ID_0, ID_1, ID_2)
                if ID == YAML["ADAPTERS"][adapter]["ID"]:
                    find_adapter = adapter
                    result = True
                    break
                else:
                    find_adapter = "Not Connected"
                    result = False

            return result, find_adapter
            
