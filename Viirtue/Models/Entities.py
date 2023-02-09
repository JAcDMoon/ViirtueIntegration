import secrets
import requests
import xmltodict


class Entities:

    def _sendRequest(self, parameters, target='', headers=''):
        url = secrets.domain + target + '?'
        for key, value in parameters.items():
            url = url + key + '=' + value + '&'
        response = requests.get(url=url, headers=headers)
        print(url)
        print(response)
        if response:
            self.__updateResponseStatus(True)
            response = self.__parseResponse(response)
            return response
        self.__updateResponseStatus(False)

    @staticmethod
    def __parseResponse(response):
        try:
            response = response.json()
            return response
        except:
            pass

        try:
            response = xmltodict.parse(response.content)
            return response
        except:
            print('===PARSE ERROR===')

    def __updateResponseStatus(self, status):
        self.__dict__.update({'status': status})
