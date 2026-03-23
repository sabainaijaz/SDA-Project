import matplotlib.pyplot as plt

def output_dashboard(processed_queue, config):
    plt.ion()

    x = []
    y = []
    avg = []

    x_key = "time"
    y_key = "value"

    show_raw = config["display"].get("show_raw", True)
    show_processed = config["display"].get("show_processed", True)

    while True:
        packet = processed_queue.get()

        if packet is None:
            break

        x.append(packet[x_key])
        y.append(packet[y_key])
        avg.append(packet.get("computed_metric", 0))

        plt.clf()

        plt_index = 1

        if show_raw:
            plt.subplot(2, 1, plt_index) 
            plt.plot(x,y)
            plt.title("Live values")
            plt_index += 1

        if show_processed:
            plt.subplot(2, 1, plt_index) 
            plt.plot(x,avg)
            plt.title("Running average")

        plt.pause(0.01)


