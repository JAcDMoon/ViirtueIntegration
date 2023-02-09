import pickle
import config


class DataBase:

    @staticmethod
    def saveDB(rewrite=False):
        mode = 'xb'
        if rewrite:
            mode = 'wb'
        with open('ApplicationDB.pickle', mode) as f:
            pickle.dump(config.AppDatabase, f)

    @staticmethod
    def loadDB():
        with open('ApplicationDB.pickle', 'rb') as f:
            return pickle.load(f)
