import matplotlib.pyplot as plt

def output_dashboard(processed_queue, config):
    plt.ion()

    x = []
    y = []
    avg = []

    x_key = config["visualizations"]["data_charts"][0]["x_axis"]
    y_key = config["visualizations"]["data_charts"][0]["y_axis"]

    while True:
        packet = processed_queue.get()

        if packet is None:
            break

        x.append(packet[x_key])
        y.append(packet[y_key])
        avg.append(packet.get("computed_metric", 0))

        plt.clf()

        plt.subplot(2, 1, 1) 
        plt.plot(x,y)
        plt.title("Live values")

        plt.subplot(2, 1, 2) 
        plt.plot(x,avg)
        plt.title("Running averagfe")

        plt.pause(0.01)


