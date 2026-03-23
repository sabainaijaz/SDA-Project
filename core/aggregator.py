from multiprocessing import Queue
from core.functional import running_average

class Aggregator:
    def __init__(self, input_queue: Queue, output_queue: Queue, window_size: int):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.window_size = window_size
        self.vals = []  # stores metric vals

    def run(self):
        while True:  
            try:

                packet = self.input_queue.get()  # blocking
                #recieves data from workwr and then stores it
                val = packet.get("metric_val")
                time = packet.get("time_period")

                if val is None:
                    continue

                # store vals in mem
                self.vals.append(val)

                # fucntinal ccall
                avg_vals = running_average(self.vals, self.window_size)

                # sned the packet to output
                outPacket = {
                    "time_period": time,
                     "metric_val": val,
                    "computed_metric": avg_vals[-1]  # latest  avdg
                }

                self.output_queue.put(outPacket)
            except Exception as e:
                print(f"Aggregator module error: {e}")  