from datetime import timedelta

class Anomaly():
    def __init__(self, name, dim_val, day_wise_averages, ref_date):
        self.name = name
        self.dim_val = dim_val
        self.day_wise_averages = day_wise_averages
        self.ref_date = ref_date

    def print_anomaly(self, name, val1, val2):
        print(self.name, self.dim_val, end=' ')
        #print("{:2.2f} {:2.2f}".format(val1, val2), end=' ')
        for i in range(1, 7):
            print("{:2.2f}".format(self.day_wise_averages[self.ref_date-timedelta(i)]), end=' ')
        print()

    def jsonify(self):
        output = {}
        output['message'] = self.name + ' on ' + self.dim_val
        output['data'] = []
        keys = sorted(self.day_wise_averages.keys())
        for key in keys:
            output['data'].append({'name': str(key), 
                                   'cpu': round(self.day_wise_averages[key], 2)})
        return output
