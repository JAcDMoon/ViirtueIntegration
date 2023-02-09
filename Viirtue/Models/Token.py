from .Entities import Entities


class Token(Entities):

    def __init__(self, grant_type, client_id, client_secret, username, grant_value):
        self.__target = 'oauth2/token/'
        self.__parameters = {'grant_type': grant_type, 'client_id': client_id, 'client_secret': client_secret, 'username': username, grant_type: grant_value}

        try:
            response = super()._sendRequest(self.__parameters, self.__target)
            self.__dict__.update(response)
        except:
            print('===TOKEN RESPONSE ERROR===')
