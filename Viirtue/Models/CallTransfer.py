from .Entities import Entities

class CallTransfer(Entities):

    def __init__(self, target, action, token, callid, uid, destination):
        self.headers = {'Authorization': 'Bearer ' + token}
        self.__parameters = {'object': target, 'action': action, 'callid': callid, 'uid': uid, 'destination': destination}

        try:
            response = super()._sendRequest(self.__parameters, '', self.headers)
            self.__dict__.update(response['xml'][''])
        except:
            print('===CALL TRANSFER ERROR===')