import matplotlib.pyplot as plt

def output_dashboard(queue, config):
    plt.ion()

    charts = config["visualizations"]["data_charts"]

    x_vals = []
    y_vals = []
    avg_vals = []

    while True:
        packet = queue.get()

        x_vals.append(packet[charts[0]["x_axis"]])
        y_vals.append(packet[charts[0]["y_axis"]])
        avg_vals.append(packet.get("computed_metric"))

        plt.clf()

        plt.subplot(2, 1, 1)
        plt.plot(x_vals, y_vals)
        plt.title("Live Values")

        plt.subplot(2, 1, 2)
        plt.plot(x_vals, avg_vals)
        plt.title("Running Average")

        plt.pause(0.01)