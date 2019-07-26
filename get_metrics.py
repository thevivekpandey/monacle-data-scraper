import datetime
import json
import boto3
from pymongo import MongoClient

def get_metric_statistics(client):
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=2)
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': 'i-0aef6289a972c932f'
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'])
    return response

def insert_to_mongo(response):
    
    
if __name__ == '__main__':
    client = boto3.client('cloudwatch')
    response = get_metric_statistics(client)
    insert_to_mongo(response)
