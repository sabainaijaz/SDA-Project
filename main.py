from multiprocessing import Process, Queue
import json

from input import Input
from core.worker import Worker
from core.aggregator import Aggregator
from output.dashboard import output_dashboard

def main():
    with open("config.json") as f:
        config = json.load(f)

    qsize = config["pipeline_dynamics"]["stream_queue_max_size"]

    raw_q = Queue(maxsize=qsize)
    proc_q = Queue(maxsize=qsize)
    final_q = Queue(maxsize=qsize)

    input_p = Process(target=Input(config, raw_q).run)

    workers = [
        Process(target=Worker(
            raw_q,
            proc_q,
            config["processing"]["stateless_tasks"]["secret_key"],
            config["processing"]["stateless_tasks"]["iterations"]
        ).run)
        for _ in range(config["pipeline_dynamics"]["core_parallelism"])
    ]

    agg_p = Process(target=Aggregator(
        proc_q,
        final_q,
        config["processing"]["stateful_tasks"]["running_average_window_size"]
    ).run)

    dash_p = Process(target=output_dashboard, args=(final_q, config), daemon=True)

    processes = [input_p] + workers + [agg_p, dash_p]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()