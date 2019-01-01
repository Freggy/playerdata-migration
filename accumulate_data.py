import json
import luigi
import pymysql.cursors
from luigi import Parameter, LocalTarget

from gather_uuids import GatheringTask


class AccumulationTask(luigi.Task):
    db_host = Parameter()
    db_user = Parameter()
    db_pass = Parameter()
    db_name = Parameter()

    def requires(self):
        return GatheringTask(self.param_kwargs)

    def run(self):
        with open("/etc/playerdata/uuids.json") as file:
            uuids = json.load(file)

        connection = pymysql.connect(host=self.db_host,
                                     user=self.db_user,
                                     passwd=self.db_pass,
                                     db=self.db_name)
        try:
            with connection.cursor() as cursor:
                for uuid in uuids:
                    print(uuid) # TODO: gather all minigames stats and put them into one json object
        finally:
            connection.close()

    def output(self):
        return LocalTarget("/etc/playerdata/accumulation.json")