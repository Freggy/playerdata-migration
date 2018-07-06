import json
import luigi
from luigi import Parameter, LocalTarget


class GatherTask(luigi.Task):
    db_host = Parameter()
    db_user = Parameter()
    db_pass = Parameter()
    db_name = Parameter()

    def run(self):
        database = MySQLdb.connect(host=self.db_host,
                                   user=self.db_user,
                                   passwd=self.db_pass,
                                   db=self.db_name)
        cursor = database.cursor()
        cursor.execute("SELECT * FROM data DISTINCT uuid")

        uuids = []

        for row in cursor.fetchall():
            uuids.append({"uuid": row[0]})

        with open(self.output().path, "w") as out:
            json.dump(uuids, out)

    def output(self):
        return LocalTarget("/etc/playerdata/uuids.json")