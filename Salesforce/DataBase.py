import sqlite3
from .DataCollector import DataCollector


class DataBase:
    def __init__(self, needToCreate=False):
        self.__DBName = 'viirtueDB'

        if needToCreate:
            self.__connect()
            self.__cursor()
            status = self.__createDB()
            if status:
                self.__DC = DataCollector()
                self.__insertParties(self.__DC.collectParties())
                self.__insertIntakes(self.__DC.collectIntakes())
            self.__commit()
            self.__close()

    def __connect(self):
        self.con = sqlite3.connect(self.__DBName)

    def __cursor(self):
        self.cur = self.con.cursor()

    def __commit(self):
        self.con.commit()

    def __close(self):
        self.con.close()

    def __createDB(self):
        try:
            self.cur.execute("CREATE TABLE parties(id TEXT PRIMARY KEY, mobile_phone INTEGER, home_phone INTEGER, "
                             "phone INTEGER, status TEXT)")
            return True
        except:
            return False

    def __insertParties(self, parties):
        for party in parties:
            self.cur.execute(f"""
                INSERT INTO parties VALUES
                ('{party['Id']}', '{party['litify_pm__Phone_Mobile__c']}', '{party['litify_pm__Phone_Home__c']}', '{party['Phone']}', '')
            """)

    def __insertIntakes(self, intakes):
        for intake in intakes:
            self.cur.execute(f"""
                            UPDATE parties SET status = '{intake['litify_pm__Status__c']}'
                            WHERE id = '{intake['litify_pm__Client__c']}'
            """)

    def partiesTriggerEvent(self, party):
        self.__connect()
        self.__cursor()

        try:
            self.cur.execute(f"""
                INSERT INTO parties VALUES
                ('{party.id}', '{party.mobile_phone}', '{party.home_phone}', '{party.phone}', '')
            """)
        except:
            self.cur.execute(f"""
                            UPDATE parties SET mobile_phone = '{party.mobile_phone}',
                            home_phone = '{party.home_phone}', phone = '{party.phone}'
                            WHERE id = '{party.id}'
            """)

        self.__commit()
        self.__close()

    def intakesTriggerEvent(self, intake):
        try:
            self.__connect()
            self.__cursor()
            self.cur.execute(f"""
                UPDATE parties SET status = '{intake.status}'
                WHERE id = '{intake.id}'
            """)
            self.__commit()
            self.__close()
        except:
            pass

    def executeSelectQuery(self, query):
        self.__connect()
        self.__cursor()
        result = self.cur.execute(query).fetchall()
        self.__commit()
        self.__close()
        return result
