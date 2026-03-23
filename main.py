from multiprocessing import Process, Queue
import json

from input import Input
from core.worker import Worker
from core.aggregator import Aggregator
from output.dashboard import output_dashboard
from output.telemetry_view import Telemetry
from monitor import Monitor, run_monitor
from telemetry import PipelineTelemetry

def main():
    with open("config.json") as f:
        config = json.load(f)

    max_size = config["pipeline_dynamics"]["stream_queue_max_size"]

    raw_queue = Queue(maxsize=max_size)
    processed_queue = Queue(maxsize=max_size)
    final_queue = Queue(maxsize=max_size)

    input_module = Input(config, raw_queue)

    workers = [
        Worker(
            raw_queue,
            processed_queue,
            config["processing"]["stateless_tasks"]["secret_key"],
            config["processing"]["stateless_tasks"]["iterations"]
        )
        for _ in range(config["pipeline_dynamics"]["core_parallelism"])
    ]

    aggregator = Aggregator(
        processed_queue,
        final_queue,
        config["processing"]["stateful_tasks"]["running_average_window_size"]
    )

    processes = []

    # Input process
    processes.append(Process(target=input_module.run))

    # Worker processes
    processes.extend([Process(target=w.run) for w in workers])

    # Aggregator process
    processes.append(Process(target=aggregator.run))

    # Dashboard process
    processes.append(Process(target=output_dashboard, args=(final_queue, config), daemon=True))

    # Telemetry Observer
    pipeline_telemetry = PipelineTelemetry(raw_queue, processed_queue)
    monitor = Monitor(pipeline_telemetry)
    telemetry_view = Telemetry(max_size)
    monitor.subscribe(telemetry_view)

    # Monitor process
    processes.append(Process(target=run_monitor, args=(monitor,), daemon=True))

    # Start all processes
    for p in processes:
        p.start()

    # Optional: wait for all processes to finish (if some are not daemons)
    for p in processes:
        p.join()


if __name__ == "__main__":
    main()