from core.functional import running_average

class Aggregator:
    def __init__(self, in_q, out_q, window):
        self.in_q = in_q
        self.out_q = out_q
        self.window = window
        self.values = []

    def run(self):
        while True:
            packet = self.in_q.get()

            value = packet["metric_value"]
            time = packet["time_period"]

            self.values.append(value)

            averages = running_average(self.values, self.window)

            out = {
                "time_period": time,
                "metric_value": value,
                "computed_metric": averages[-1]
            }

            self.out_q.put(out)