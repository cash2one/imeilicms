
from enum import Enum
from pymongo import MongoClient
class Imeili100ResultStatus(Enum):
        ok = 0
        failed = 1


class Imeili100Result():
    def __init__(self):
        self.status = Imeili100ResultStatus.ok.value
        self.res = None
        self.msg = "成功"


