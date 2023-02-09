import config
import time
from .Models import *
# todo
import Salesforce
import secrets



class RequestProcessor:
    def __init__(self):
        self.viirtueTokenObject = ''
        self.viirtueSubscribeObject = ''

    def __getViirtueTokenObject(self):
        if  self.viirtueTokenObject and self.viirtueTokenObject.refresh_token:
            self.viirtueTokenObject = Token('refresh_token', secrets.client_id, secrets.client_secret, secrets.username, self.viirtueTokenObject.refresh_token)
            config.globalToken = self.viirtueTokenObject.access_token
            return

        self.viirtueTokenObject = Token('password', secrets.client_id, secrets.client_secret, secrets.username, secrets.user_password)
        config.globalToken = self.viirtueTokenObject.access_token
        return

    def __updateSubscribe(self):
        self.viirtueSubscribeObject = Subscription('event', 'create', self.viirtueTokenObject.access_token, 'call', secrets.local_url, self.viirtueTokenObject.domain)

    def startProcessor(self):
        self.__getViirtueTokenObject()
        self.__updateSubscribe()
        print(self.viirtueSubscribeObject.expires)
        print(config.globalToken)
        time.sleep(3200)
        self.startProcessor()

    @staticmethod
    def transferCall(token, number, callid):
            # todo
            destination = RequestProcessor.__getDestination(number)
            transfer = CallTransfer('call', 'xfer', token, callid, secrets.uid_for_transfer, destination)

    @staticmethod
    def conditionsAreRight(number):

        phoneNumberDataBase = Salesforce.DataBase()
        isMatch = phoneNumberDataBase.executeSelectQuery(f"""SELECT id FROM parties WHERE (mobile_phone LIKE '%{number}%' OR 
                home_phone LIKE '%{number}%' OR phone LIKE '%{number}%') AND status NOT IN ("Open", "Pending Intake", "Pending Retainer Only",
                                                                  "Retainer Agreement Sent")""")

        if isMatch:
            return True
        return False

    # todo
    @staticmethod
    def __getDestination(number):
        return '999@Broderick'