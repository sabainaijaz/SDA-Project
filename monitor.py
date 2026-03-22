import time

class monitor:
    def __init__(self, telemetry):
        self.telemetry = telemetry
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def notify(self):
        data = self.telemetry.get_status()
        list(map(lambda obs: obs.update(data), self.observers))

def run_monitor(monitor, interval=1):
    while True:
        monitor.notify()
        time.sleep(interval)

        