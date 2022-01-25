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
            #print("PACKET")
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
            """To get status of wanted INPUT pins -> returns list in form of string like 100 -> means MSB is 1, LSB is 0  """
            [status,message] = self.NormalCommand("READPINS")#return status of all input pins
            if status == True: 
                #parse response to get status of wanted pins
                raw_ID_list = message.split(";")
                ID_POS_2_LSB = int(INPUT_PIN_0_LSB[-1:])
                ID_POS_1 = int(INPUT_PIN_1[-1:])
                ID_POS_0_MSB = int(INPUT_PIN_2_MSB[-1:])
                ID_of_adapter = raw_ID_list[ID_POS_0_MSB - 1] + raw_ID_list[ID_POS_1 - 1] + raw_ID_list[ID_POS_2_LSB - 1]
                #print("ADAPTER ID IS: ", ID_of_adapter)
                return status,ID_of_adapter
        
        def GetNeedleinStates(self,connected_adapter,YAML): #in form of string "IN_1", "IN_4", etc.. 
            """Give me, which adapter is connected and YAML with following structure:
            ADAPTERS:
                ADAPTER_1:
                    CONFIGURATION:
                        PINOUT:
                            SWITCH_NEEDLE_A #This represents position for DUT
                            SWITCH_NEEDLE_B #please fill also these position even if there is less physical positions in adapter..
                            SWITCH_NEEDLE_C
                ADAPTER_2....
            
            And I will return you status of needles in form of list like [1,1,0],
            please note, that status is negated, due to the common wiring in ACTIVE LOW format.."""
                            
            [status,message] = self.NormalCommand("READPINS")
            if status == True:
                raw_ID_list = message.split(";")
                #print(connected_adapter)
                POS_A = int(YAML["ADAPTERS"][connected_adapter]["CONFIGURATION"]["PINOUT"]["SWITCH_NEEDLE_A"][-1:])
                POS_B = int(YAML["ADAPTERS"][connected_adapter]["CONFIGURATION"]["PINOUT"]["SWITCH_NEEDLE_B"][-1:])
                POS_C = int(YAML["ADAPTERS"][connected_adapter]["CONFIGURATION"]["PINOUT"]["SWITCH_NEEDLE_C"][-1:])
                try:
                    #print(raw_ID_list)
                    needle_state = [not int(raw_ID_list[POS_A - 1][-1:]), not int(raw_ID_list[POS_B - 1]) , not int(raw_ID_list[POS_C - 1])]
                    #print("SWITCH NEEDLE STATE IS:", needle_state)
                    return status,needle_state
                
                except:
                    return "BUG",[0, 0, 0]

        def GetConnectedAdapter(self, YAML): #YAML is YAML config file
            """returns which adapter is connected based on .yaml file, which should have structure defined as follows:
            ADAPTERS:
                ADAPTER_1:
                    CONFIGURATION
                        PINOUT
                            ID_PIN_0 : IN_4 #ARRIGO INPUT PIN, where ID detection is connected
                            ID_PIN_1 : IN_5
                            ID_PIN_2 : IN_6

                ADAPTER_2....
                """
            find_adapter = ""
            all_adapters = []
            for i in range (0,YAML["ADAPTERS"]["TOTAL_NUMBER_OF_ADAPTERS"]):
                all_adapters.append("ADAPTER_" +  str(i+1) )
            for adapter in all_adapters: # for each adapter in YAML file get ID_PINS of ARRIGO
                ID_2 = YAML["ADAPTERS"][adapter]["CONFIGURATION"]["PINOUT"]["ID_PIN_2"]
                ID_1 = YAML["ADAPTERS"][adapter]["CONFIGURATION"]["PINOUT"]["ID_PIN_1"]
                ID_0 = YAML["ADAPTERS"][adapter]["CONFIGURATION"]["PINOUT"]["ID_PIN_0"]
                [status, ID] = self.GetIdPinStates(ID_0, ID_1, ID_2)
                #print(ID)
                if ID == YAML["ADAPTERS"][adapter]["ID"]: #IF ID MATCH
                    find_adapter = adapter
                    result = True
                    
                    break
                else:
                    find_adapter = "Not Connected"
                    result = False

            return result, find_adapter

        def SetExtPort(self,EXT,vector, On_Off, current_state):
            #This function change EXT port accordingly to the vector
            #vector is a string of 1 and 0 like this LSB 000000000000000111000000 MSB (32 bit for 32 bit relay card)
            #If instead of str vector is int input, this will change only 1 pin
            #Function will set pins from vector asigned as 1 to Off or ON state according to the On_Off state
            # and will not affect another pins,
            if type(vector) == str: 
                to_set_value = vector #1111100000000000000000000
                if On_Off == True:
                    new_state =  int(current_state,2) | int(to_set_value,2)
                else:
                    new_state =  int(current_state,2) & (~int(to_set_value,2))

            elif type(vector) == int:
                if On_Off == True:
                    new_state = (int(current_state,2)) | (1<< 32 -vector)
                else:
                    new_state =  int(current_state,2) & (~(1<< 32 - vector))
            
            new_state = bin(new_state)[2:].zfill(32) #get rid of 0b and fill with 0 to 32 bit length
            to_send_string = to_set_string = ';'.join(new_state[i:i + 1] for i in range(0, len(new_state)))
            [status, message] = self.NormalCommand("SETEXTPORT;"+ str(EXT) + ";" + to_send_string)
            current_state = new_state
            return status,message,current_state
            
