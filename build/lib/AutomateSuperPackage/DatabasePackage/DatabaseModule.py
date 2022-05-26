from AutomateSuperPackage.DatabasePackage.AccesDatabasePackage.AccesDatabaseModule import AccesDatabaseClass
from AutomateSuperPackage.DatabasePackage.SoapWsPackage.SoapWsModule import SoapWsClass
class DatabaseClass:
    def __init__(self):
        self.AccesDatabase = AccesDatabaseClass()
        print( "IM Database CLASS ")

        self.SoapWs = SoapWsClass()
        print( "IM SoapWS CLASS ")

    def FOO():
        ...

    
