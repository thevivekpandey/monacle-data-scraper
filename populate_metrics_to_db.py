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
            print(metric)
            ns = config['Namespace']
            dim_name = config['Dimensions'][0]['Name']
            metric_name = config['MetricName']
            dim_value = metric['Dimensions'][0]['Value']
            stats = config['Stats']
            insert_data = {'ns': ns, 'dim_name': dim_name, 'dim_value': dim_value, 'metric': metric_name, 'period': 300, 'stats': stats}
            db.insert_fetch_config(insert_data)
        f = open('/home/ubuntu/log/populate_metrics_to_db.txt', 'a')
        f.write(f"Put {len(response['Metrics'])} metrics in mysql db\n")
        f.close()
    
if __name__ == '__main__':
    while True:
        db = database.Database(0)
        ids_2_credentials = db.get_credentials()
        for id, credentials in ids_2_credentials.items():
            print(id)
            db = database.Database(id)
            key = credentials['aws_access_key_id']
            secret = credentials['aws_secret_access_key']
            cloudwatch = boto3.client('cloudwatch', 
                                      aws_access_key_id=key, 
                                      aws_secret_access_key=secret)
            paginator = cloudwatch.get_paginator('list_metrics')

            for config in CONFIGS:
                process_one_config(paginator, config, db)
        print('Sleeping now')
        time.sleep(3600)
