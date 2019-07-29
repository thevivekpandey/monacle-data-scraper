import database
import boto3
import time

CONFIGS = [
        {'Namespace': 'AWS/EC2',            
         'MetricName': 'CPUUtilization', 
         'Dimensions': [{'Name': 'InstanceId'}],            
         'Stats': 'Average'},
        {'Namespace': 'AWS/ApplicationELB', 
         'MetricName': 'RequestCount',   
         'Dimensions': [{'Name': 'TargetGroup'}],
         'Stats': 'Sum'},
        {'Namespace': 'AWS/ApplicationELB', 
         'MetricName': 'HTTPCode_ELB_5XX_Count',    
         'Dimensions': [{'Name': 'LoadBalancer'}], 
         'Stats': 'Sum'}
]

def process_one_config(paginator, config, db):
    for response in paginator.paginate(MetricName=config['MetricName'],
                                       Namespace=config['Namespace'],
                                       Dimensions=config['Dimensions']):
        for metric in response['Metrics']:
            ns = config['Namespace']
            dim_name = config['Dimensions'][0]['Name']
            metric_name = config['MetricName']
            dim_value = metric['Dimensions'][0]['Value']
            stats = config['Stats']
            insert_data = {'ns': ns, 'dim_name': dim_name, 'dim_value': dim_value, 'metric': metric_name, 'period': 300, 'stats': stats}
            db.insert_fetch_config(insert_data)
    
if __name__ == '__main__':
    cloudwatch = boto3.client('cloudwatch')
    paginator = cloudwatch.get_paginator('list_metrics')
    db = database.Database()

    while True:
        for config in CONFIGS:
            process_one_config(paginator, config, db)
        time.sleep(3600)
