import os
from dotenv import load_dotenv

load_dotenv('.env')


class Config():
    '''Config env'''
    _instance = None
    env = dict(os.environ)

    def getConfig(self):
        '''Load os env'''
        if self._instance == None:
            _instance = Config()
        return _instance
