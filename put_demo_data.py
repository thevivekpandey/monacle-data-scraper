import yaml
import re
from database import Database
from datetime import datetime, timedelta

def insert_one_anomaly(fname, db):
    with open(fname) as f:
        chart_data = f.read()
    
    regex = r'{[a-zA-Z0-9_ ]+}'
    matches = re.findall(regex, chart_data)
    for match in matches:
        macro = match[1:-1]
        delta, unit = macro.split(' ')
        if unit == 'HR':
            output = datetime.now() - timedelta(hours=int(delta))
            output -= timedelta(minutes=output.minute, seconds=output.second, microseconds=output.microsecond)
            output_str = output.strftime("%b %d, %H:%M")
        elif unit == 'DAY':
            output = datetime.now() - timedelta(days=int(delta))
            output_str = output.strftime("%b %d")
        chart_data = chart_data.replace(match, output_str)
    
    chart_data = yaml.load(chart_data)
    
    db.write_anomaly(chart_data)

if __name__ == '__main__':
    db = Database(13)
    db.clear_anomalies()
    insert_one_anomaly('demo_data.yml', db)
    insert_one_anomaly('demo_data_2.yml', db)
