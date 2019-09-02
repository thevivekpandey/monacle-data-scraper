from datetime import datetime
from datetime import timedelta
import uuid
import json
import boto3
import time
import database
from pymongo import MongoClient

def get_start_end_time():
    end_time = datetime.now()
    end_min = end_time.minute
    end_time = end_time.replace(minute=end_min - end_min % 5, second=0, microsecond=0)
    start_time = end_time - timedelta(days=3)
    return start_time, end_time

def get_metric_statistics(client, config):
    start_time, end_time = get_start_end_time()
    response = client.get_metric_statistics(
        Namespace=config['namespace'],
        MetricName=config['metric'],
        Dimensions=[{
            'Name': config['dim_name'],
            'Value': config['dim_value']
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=config['period'],
        Statistics=[config['stats']])
    return response

def insert_to_mongo(config, response, app_id):
    conn = MongoClient('localhost')
    data = conn[app_id].data

    inserted = 0
    for datapoint in response['Datapoints']:
        ts = datapoint['Timestamp']
        val = datapoint[config['stats']]
        doc = {
            'ts': ts,
            'ns': config['namespace'],
            'metric': config['metric'],
            'dimName': config['dim_name'],
            'dimVal': config['dim_value'],
            'metricVal': val,
            'mTime': datetime.now()
        }
        query = {
                 'ns': config['namespace'], 
                 'metric': config['metric'], 
                 'dimName': config['dim_name'],
                 'dimVal': config['dim_value'],
                 'ts': ts
                }
        data.update(query, doc, upsert=True)
        inserted += 1
    return inserted

if __name__ == '__main__':
    while True:
        db = database.Database(0)
        ids_2_credentials = db.get_credentials()
        ids_2_app_id = db.get_id_app_id_mapping()

        for id, credentials in ids_2_credentials.items():
            print(id)
            f = open('/home/ubuntu/log/scrape.txt', 'a')
            db = database.Database(id)
            key = credentials['aws_access_key_id']
            secret = credentials['aws_secret_access_key']
            client = boto3.client('cloudwatch', aws_access_key_id=key, aws_secret_access_key=secret)
            app_id = ids_2_app_id[id]
            configs = db.get_metrics()
            inserted = 0
            for idx, config in enumerate(configs):
                response = get_metric_statistics(client, config)
                inserted += insert_to_mongo(config, response, app_id)
                if idx % 10 == 0:
                    print(idx, "/", len(configs))
                    f.write(f"idx = {idx}\n")
            f.write(f"Did one round, inserted {inserted} rows, sleeping now\n")
            f.close()
        time.sleep(300)
