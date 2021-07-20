import io
import os
import pyodbc
class AccesDatabaseClass:
    def __init__(self):
        print("IM AccesDatabaseClass")

    def SimplyConnectByPath(self,path):
        self.dBpath = os.path.abspath(path)
        self.ConnectionString = "Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + self.dBpath + ";"
        self.connection = pyodbc.connect(self.ConnectionString)
        self.cursor = self.connection.cursor()

    def WriteQuery(self, QueryString):
        self.Query = QueryString
        self.cursor.execute(self.Query)

    def ResultFromQuery(self):
        self.QueryResult = self.cursor.fetchall()
        return self.QueryResult

    def UpdateDatabase(self):
        self.cursor.commit()

    class MyOLEObject:
        exists = "NO"
        def __init__(self):
            self.exists = "YES"
            

        def DebugFile(outputFileName,ext):
            #FOR DEBUGING and future addions create also raw binary file to compare wit source file
            with open(outputFileName, "rb") as f:
                buffer = io.BytesIO(f.read())
                f.close()
            
            with open("ItIs"+ext, "w") as f: ##output ItIs.ext file (Readabble RAW STRING file for debuging)
                f.write(str(buffer.read()))
                f.close()


        def GetJpgFile(self,QUERY_RESULT,outputFileName):
            posOFExtension = outputFileName.rfind(".") 
            ext = outputFileName[posOFExtension:] #get extension from file name
            posOfHeaderEnd = QUERY_RESULT.find(b'\x1cICC_PROFILE') - 5 #removing header from MSACCESSDB
            outBytes = io.BytesIO(QUERY_RESULT[posOfHeaderEnd:])
            with open(outputFileName, "wb") as f:
                f.write(outBytes.getbuffer())
                f.close()

            self.DebugFile(outputFileName,ext)

        def GetTxtFile(self,QUERY_RESULT,outputFileName):#OLE Object from QUERY
            posOFExtension = outputFileName.rfind(".") 
            ext = outputFileName[posOFExtension:] #get extension from file name 
            extension = ext.encode() #needed to string.find()
            #there are 3 .ext headers before...
            posOfHeaderEnd = QUERY_RESULT.find(extension)  #removing header from MSACCESSDB
            posOfHeaderEnd = QUERY_RESULT.find(extension,posOfHeaderEnd+1)  #removing header from MSACCESSDB
            posOfHeaderEnd = QUERY_RESULT.find(extension,posOfHeaderEnd+1)  #removing header from MSACCESSDB
            posOfHeaderEnd += 9 # offset from last .ext
            
            if ext == ".FRB" or ext == ".frb":
                EndPOS = QUERY_RESULT.rfind(b'\x01Z')
                outBytes = io.BytesIO(QUERY_RESULT[posOfHeaderEnd:EndPOS+4])

            elif ext == ".FRS" or ext == ".FRS" or ext == ".txt" or ext == ".TXT":
                EndPOS = QUERY_RESULT.rfind(b'\x00:')
                EndPOS = QUERY_RESULT.rfind(b'\x00:',0 ,EndPOS-1)
                outBytes = io.BytesIO(QUERY_RESULT[posOfHeaderEnd:EndPOS-4][0:-1])
            else:
                print("UNKOWN DATATYPE (SUPPORT: FRS,FRB,JPEG,TXT)")
                return

            #Save final result into file
            #print(EndPOS)   
            with open(outputFileName, "wb") as f:
                f.write(outBytes.getbuffer())
                f.close()
            
            self.DebugFile(outputFileName,ext)

