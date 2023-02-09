from simple_salesforce import Salesforce, format_soql
from secrets import salesforce as sfSecrets
import re


class DataCollector:

    def __init__(self):
        self.sf = Salesforce(domain='test', username=sfSecrets['username'], password=sfSecrets['password'],
                             consumer_key=sfSecrets['client_id'], consumer_secret=sfSecrets['client_secret'])

    @staticmethod
    def findPhone(phone):
        incorrectSymbols = ['-', '+', '=', '(', '(', ')', ' ', '']

        try:
            for i in incorrectSymbols:
                phone = phone.replace(i, '')

            phone = re.search(r'\d{1,}', phone).group()
            return phone
        except:
            return False

    def collectIntakes(self):

        intakes = self.sf.query_all(format_soql("SELECT litify_pm__Client__c, litify_pm__Status__c FROM "
                                                "litify_pm__Intake__c WHERE litify_pm__Status__c IN {someList}",
                                                someList=["Open", "Pending Intake", "Pending Retainer Only",
                                                          "Retainer Agreement Sent"]))['records']
        return intakes

    def collectParties(self):

        parties = self.sf.query_all(format_soql("SELECT Id, litify_pm__Phone_Mobile__c, litify_pm__Phone_Home__c, "
                                                "Phone FROM Account WHERE litify_pm__Phone_Mobile__c != null OR "
                                                "litify_pm__Phone_Home__c != null OR Phone != null"))['records']

        for party in parties:
            delete = True

            mobile_phone = self.findPhone(party['litify_pm__Phone_Mobile__c'])
            home_phone = self.findPhone(party['litify_pm__Phone_Home__c'])
            phone = self.findPhone(party['Phone'])

            if mobile_phone:
                party['litify_pm__Phone_Mobile__c'] = mobile_phone
                delete = False

            if home_phone:
                party['litify_pm__Phone_Home__c'] = home_phone
                delete = False

            if phone:
                party['Phone'] = phone
                delete = False

            if delete:
                parties.remove(party)

        return parties
