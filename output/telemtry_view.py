import matplotlib.pyplot as plt

def get_color(ratio):
    if ratio < 0.5:
        return "green"
    elif ratio < 0.8:
        return "yellow"
    else:
        return "red"

class TelemetryView:
    def __init__(self, max_size):
        self.max_size = max_size
        plt.ion()

    def update(self, data):
        raw_size, process_size = data 

        raw_ratio = raw_size / self.max_size
        process_ratio = process_size / self.max_size

        raw_color = get_color(raw_ratio)
        process_color = get_color(process_ratio)

        plt.figure(1)
        plt.clf()

        plt.bar(["Raw Queue"], [raw_size], color=raw_color)
        plt.bar(["Processed Queue"], [process_size], color=process_color)

        plt.title("Pipeline Telemetry")
        plt.ylabel("Queue Size")

        plt.pause(0.01)
          
