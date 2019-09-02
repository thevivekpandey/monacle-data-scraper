import MySQLdb
from datetime import datetime
import json

class Database:
    def __init__(self, account_id):
        db = MySQLdb.connect(host='localhost',
                             user='root',
                             passwd='root',
                             db='monacle')
        self.account_id = account_id
        self.conn = db
        self.cursor = db.cursor()
        self.dictcursor = db.cursor(MySQLdb.cursors.DictCursor)

    def get_metrics(self):
        query = f"select namespace, metric, dim_name, dim_value, period, stats from scrape_config where account_id = {self.account_id} and deleted = 0"
        self.dictcursor.execute(query)
        return self.dictcursor.fetchall()

    def insert_fetch_config(self, config):
        query = f"replace into scrape_config (account_id, namespace, metric, dim_name, dim_value, period, stats) values ({self.account_id}, \"{config['ns']}\", \"{config['metric']}\", \"{config['dim_name']}\", \"{config['dim_value']}\", {config['period']}, \"{config['stats']}\")"
        self.cursor.execute(query)
        self.cursor.connection.commit()
        print(datetime.now(), query)

    def clear_anomalies(self, account_id):
        print('clearning anomalies')
        query = f"delete from api_feed where account_id = {account_id}"
        self.cursor.execute(query)
        self.cursor.connection.commit()

    def write_anomaly(self, account_id, anomaly):
        print('doing querying')
        query = "insert into api_feed (feed, account_id, deleted) values (%s, %s, %s)"
        print(query)
        self.cursor.execute(query, (json.dumps(anomaly), 1, 0))
        self.cursor.connection.commit()
        print('done querying')

    def get_credentials(self):
        query = "select id, settings from api_account where settings like '%aws_access_key_id%'";
        self.dictcursor.execute(query)
        credentials = {}
        for item in self.dictcursor.fetchall():
            id = item['id']
            settings = json.loads(item['settings'])
            key = settings['aws_access_key_id']
            secret = settings['aws_secret_access_key']
            region = settings['region']
            credentials[id] = {
                'aws_access_key_id': key,
                'aws_secret_access_key': secret,
                'region': region
            }
        return credentials

    def get_id_app_id_mapping(self):
        query = "select id, app_id from api_account";
        self.dictcursor.execute(query)
        id_2_app_id = {}
        for item in self.dictcursor.fetchall():
            id = item['id']
            app_id = item['app_id']
            id_2_app_id[id] = app_id
        return id_2_app_id

if __name__ == '__main__':
    db = Database(0)
    print(db.get_id_app_id_mapping())
