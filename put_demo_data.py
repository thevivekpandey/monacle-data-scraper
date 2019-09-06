import yaml
import re
from database import Database
from datetime import datetime, timedelta

def format_monospace(in_text, match):
    output = '<span style="font-style: monospace"><a href="#">' + match[1:-1] + '</a></span>'
    x = in_text.replace(match, output)
    return x

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

    regex = r'\[[a-zA-Z0-9_-]+\]'
    matches = re.findall(regex, chart_data)
    for match in matches:
        chart_data = format_monospace(chart_data, match)

    chart_data = yaml.load(chart_data)
    
    db.write_anomaly(chart_data)

if __name__ == '__main__':
    db = Database(13)
    db.clear_anomalies()
    insert_one_anomaly('demo_data_1.yml', db)
    insert_one_anomaly('demo_data_2.yml', db)
    insert_one_anomaly('demo_data_3.yml', db)
    insert_one_anomaly('demo_data_4.yml', db)
    insert_one_anomaly('demo_data_5.yml', db)
