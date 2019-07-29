import MySQLdb
from datetime import datetime

class Database:
    def __init__(self):
        db = MySQLdb.connect(host='localhost',
                             user='root',
                             passwd='root',
                             db='monacle')
        self.client_id = 1
        self.conn = db
        self.cursor = db.cursor()
        self.dictcursor = db.cursor(MySQLdb.cursors.DictCursor)

    def get_metrics(self):
        query = f"select namespace, metric, dim_name, dim_value, period, stats from scrape_config where client_id = {self.client_id} and deleted = 0"
        self.dictcursor.execute(query)
        return self.dictcursor.fetchall()

    def insert_fetch_config(self, config):
        query = f"replace into scrape_config (client_id, namespace, metric, dim_name, dim_value, period, stats) values ({self.client_id}, \"{config['ns']}\", \"{config['metric']}\", \"{config['dim_name']}\", \"{config['dim_value']}\", {config['period']}, \"{config['stats']}\")"
        self.cursor.execute(query)
        self.cursor.connection.commit()
        print(datetime.now(), query)

if __name__ == '__main__':
    db = Database()
    print(db.get_metrics(1))
