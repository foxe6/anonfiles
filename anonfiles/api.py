import requests
import sqlq
import time
from omnitools import p


__ALL__ = ["AnonFiles", "BayFiles", "ForumFiles"]


class BaseFiles(object):
    url = ""

    def __init__(self, db: str, token: str = "") -> None:
        if type(self) is BaseFiles:
            raise Exception(type(self).__name__+" is an abstract class")
        self.url += f"?token="+token if token else ""
        self.db = db
        self.instance = "["+type(self).__name__+"] "

    def upload(self, filename: str) -> dict:
        p(self.instance+f"<uploading> {filename} ==> {self.url}", end="")
        response = requests.post(self.url, files={"file": open(filename, "rb")}).json()
        url_short = response["data"]["file"]["url"]["short"]
        p("\r"+self.instance+f"<uploaded> {filename} ==> {url_short}")
        return response
        # issued = int(time.time())
        # uploaded = int(time.time())
        # sqlqueue = sqlq.SqlQueue(server=True, db=self.db, timeout_commit=100)
        # sql = '''CREATE TABLE IF NOT EXISTS "history" ("url" TEXT, "path" TEXT, "issued" INTEGER, "uploaded" INTEGER);'''
        # sqlqueue.sql(sql)
        # sql = '''INSERT INTO history VALUES (?, ?, ?, ?);'''
        # url_short = response["data"]["file"]["url"]["short"]
        # data = (url_short, filename, issued, uploaded)
        # sqlqueue.sql(sql, data)
        # sqlqueue.commit()
        # sqlqueue.stop()


class AnonFiles(BaseFiles):
    url = "https://api.anonfiles.com/upload"


class BayFiles(BaseFiles):
    url = "https://api.bayfiles.com/upload"


class ForumFiles(BaseFiles):
    url = "https://api.forumfiles.com/upload"

    def __init__(self, db: str):
        super().__init__(db)



