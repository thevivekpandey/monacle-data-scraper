from datetime import timedelta
from datetime import date

class AnomalyCalculator():
    def __init__(self, time_series, ref_date, dim_val):
        self.time_series = time_series
        self.ref_date = ref_date
        self.dim_val = dim_val
        self.day_wise_averages = self._calculate_day_wise_averages(time_series)

    def _add_if_no_null(self, anomalies, anomaly, dim_val):
        if anomaly:
            anomalies.append(anomaly)
        return anomalies

    def print_anomaly(self, name, val1, val2):
        print(name, self.dim_val, end=' ')
        print("{:2.2f} {:2.2f}".format(val1, val2), end=' ')
        for i in range(1, 7):
            print("{:2.2f}".format(self.day_wise_averages[self.ref_date-timedelta(i)]), end=' ')
        print()

    def _calculate_day_wise_averages(self, time_series):
        sums_counts = {}
        for t, val in self.time_series.items():
            d = t.date()
            sums_counts.setdefault(d, {'sum': 0, 'count': 0})
            sums_counts[d]['sum'] += val
            sums_counts[d]['count'] += 1
        averages = {}
        for d, detail in sums_counts.items():
            averages[d] = detail['sum'] / detail['count']
        return averages

    def _is_7_day_data_present(self):
        if any([self.ref_date - timedelta(i) not in self.day_wise_averages for i in range(0, 7)]):
            return False
        return True

    def _get_6_day_average(self):
        return sum([self.day_wise_averages[self.ref_date - timedelta(i)] for i in range(1, 7)]) / 6
    
    def _check_unusually_high_cpu(self):
        if not self._is_7_day_data_present():
            return False
        ref_val = self.day_wise_averages[self.ref_date]
        avg_of_last_6_days = self._get_6_day_average()

        cond1 = ref_val > 1.5 * avg_of_last_6_days 
        cond2 = all([ref_val > 1.3 * self.day_wise_averages[self.ref_date- timedelta(i)] for i in range(1, 7)])
        if cond1 and cond2:
            self.print_anomaly('high cpu', ref_val, avg_of_last_6_days)
            return True
        return False

    def _check_unusually_low_cpu(self):
        if not self._is_7_day_data_present():
            return False
        ref_val = self.day_wise_averages[self.ref_date]
        avg_of_last_6_days = self._get_6_day_average()

        cond1 = ref_val < 0.5 * avg_of_last_6_days 
        cond2 = all([ref_val < 0.7 * self.day_wise_averages[self.ref_date- timedelta(i)] for i in range(1, 7)])
        if cond1 and cond2:
            self.print_anomaly('low cpu ', ref_val, avg_of_last_6_days)
            return True
        return False

    def check_anomalies(self):
        functions = [self._check_unusually_high_cpu, self._check_unusually_low_cpu]
        anomalies = []
        for f in functions:
            anomaly = f()
            anomalies = self._add_if_no_null(anomalies, anomaly, self.dim_val)
        return anomalies

