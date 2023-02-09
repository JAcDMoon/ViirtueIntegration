import contextlib
import threading
import time

import uvicorn
from uvicorn import Config

import FastApi
import Salesforce
import Viirtue
import config
import secrets

# todo
salesforceDatabase = Salesforce.DataBase(needToCreate=True)

try:
    config.AppDatabase = FastApi.DataBase.loadDB()
except:
    config.AppDatabase = secrets.initialDatabase
    FastApi.DataBase.saveDB()

class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


config = Config("FastApi.api:api", port=5000, log_level="info")
server = Server(config=config)

with server.run_in_thread():
    requestProcessor = Viirtue.RequestProcessor()
    requestProcessor.startProcessor()
