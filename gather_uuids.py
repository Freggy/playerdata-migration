import json
import luigi
import pymysql.cursors
from luigi import Parameter, LocalTarget


class GatheringTask(luigi.Task):
    db_host = Parameter()
    db_user = Parameter()
    db_pass = Parameter()
    db_name = Parameter()

    def run(self):
        connection = pymysql.connect(host=self.db_host,
                                     user=self.db_user,
                                     passwd=self.db_pass,
                                     db=self.db_name)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT uuid FROM playerdata.data")
                uuids = []
                for row in cursor.fetchall():
                    uuids.append({"uuid": row[0]})
                with open(self.output().path, "w") as out:
                    json.dump(uuids, out)
        finally:
            connection.close()

    def output(self):
        return LocalTarget("/etc/playerdata/uuids.json")
