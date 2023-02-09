from .Entities import Entities


class Subscription(Entities):

    def __init__(self, target, action, token, model, post_url, domain):
        self.headers = {'Authorization': 'Bearer ' + token}
        self.__parameters = {'object': target, 'action': action, 'model': model, 'post_url': post_url, 'domain': domain}

        try:
            response = super()._sendRequest(self.__parameters, '', self.headers)
            self.__dict__.update(response['xml']['subscription'])
        except:
            print('===SUBSCRIPTION RESPONSE ERROR===')
