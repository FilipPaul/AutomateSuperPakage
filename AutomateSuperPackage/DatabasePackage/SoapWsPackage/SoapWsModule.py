from zeep.client import Client
import logging.config

#to disable DEBUG INFO
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'WARNING',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

class SoapWsClass:
    def __init__(self):
        print("Soap Services Class")
        
    def InitSoapWs(self, wsdl):
        self.client = Client(wsdl = wsdl)

    def GetPcbSnRecipe(self,station, user, SerialNumber):
        try:
            result = self.client.service.GetPcbSnRecipe(str(station), str(user),str(SerialNumber))#zeep SOAP request
            if bool(result.retStatus) == True:

                #Store Results into Dictionary
                WS_result_Dictionary = {
                    #'RetStatus': bool(result.retStatus),
                    'PRODUCT ID' : str(result.product) ,
                    'REVISION': str(result.revision),
                    'lot'     : str(result.lot),
                    }

                for dictionaries in result.recipeAttributeList.attribute:
                    if dictionaries['value'] == '?':
                        ...
                        #WS_result_Dictionary[dictionaries['name']] =  None
                    else:
                        WS_result_Dictionary[dictionaries['name']] = dictionaries['value']
                return True, WS_result_Dictionary,result.product
            
            else:
                return False, {"FAULT MSG":result.retFaultMsg},None
        except Exception as e:
            print("ERROR IN GetPcbSnRecipe, line 59, Custom function\n")
            print(e)
            return False, {"FAULT MSG":"ERROR IN GetPcbSnRecipe, line 59"},None

    def GetLotRecipe(self,station, user, SerialNumber):
        try:
            result = self.client.service.GetLotRecipe(str(station), str(user),str(SerialNumber))#zeep SOAP request
            if bool(result.retStatus) == True:

                #Store Results into Dictionary
                WS_result_Dictionary = {
                    #'RetStatus': bool(result.retStatus),
                    'PRODUCT ID' : str(result.product) ,
                    'REVISION': str(result.revision),
                    'lot'     : SerialNumber,
                    }

                for dictionaries in result.recipeAttributeList.attribute:
                    if dictionaries['value'] == '?':
                        ...
                        #WS_result_Dictionary[dictionaries['name']] =  None
                    else:
                        WS_result_Dictionary[dictionaries['name']] = dictionaries['value']
                return True, WS_result_Dictionary,result.product
            
            else:
                return False, {"FAULT MSG":result.retFaultMsg},None
        except Exception as e:
            print(e)
            return False, {"FAULT MSG":"ERROR IN GetLotSnRecipe, line 89"},None

    def SaveTestResults(self, WS_log_Dictionary):
        #Input Dictionary should be in form like this:.....

        #WS_log_Dictionary = {
        #    'station' : 'UPP Siemens Trutnov',
        #    'user'    : 'Filip Paul',
        #    'sn'      : 'LO/210823-012258',
        #    'startDateTime' : '2021-08-23T13:00:00',
        #    'endDateTime' : '2021-08-23T13:01:00',
        #    'testResult' : 'FAIL', #FAIL or PASS only
        #    'logFile'     : '2021-08-23_log.txt',
        #    'list_of_dictionaries': [{'name': 'hello', 'value': "gay"}, {'name': 'hello2', 'value': "gay2"}]
        #    }

        result = self.client.service.SaveTestResults(WS_log_Dictionary['station'],
        WS_log_Dictionary['user'],
        WS_log_Dictionary['sn'],
        WS_log_Dictionary['startDateTime'],
        WS_log_Dictionary['endDateTime'],
        WS_log_Dictionary['testResult'],
        WS_log_Dictionary['logFile'],
        {'attribute' : WS_log_Dictionary['list_of_dictionaries']})
        return result