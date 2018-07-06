import luigi as luigi
from luigi import Parameter


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
