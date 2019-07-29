from pymongo import MongoClient

class MoMongo():
    def __init__(self):
        self.conn = MongoClient('localhost')
        self.data = self.conn['test'].data

    def get_data_from_mongo(self, ns, dim_name, metric):
        query = {'ns': ns, 'metric': metric, 'dimName': dim_name}
        projection = {'ts': 1, 'metricVal': 1, 'dimVal': 1}
        results = self.data.find(query, projection)
        data =  [result for result in results]
        return data

if __name__ == '__main__':
    m = MoMongo()
    m.get_data_from_mongo('AWS/EC2', 'InstanceId', 'CPUUtilization')
