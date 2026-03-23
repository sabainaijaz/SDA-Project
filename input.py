import pandas as pd
import time


class Input:
    def __init__(self, config, output_queue):
        self.queue = output_queue
        self.config = config

        self.file_path = config["dataset_path"]
        self.schema = config["schema_mapping"]["columns"]
        self.delay = config["pipeline_dynamics"]["input_delay_seconds"]

    def cast(self, value, dtype):
        try:
            if dtype == "string":
                return str(value)
            elif dtype == "integer":
                return int(value)
            elif dtype == "float":
                return float(value)
        except:
            return None

    def map_row(self, row):
        packet = {}
        for col in self.schema:
            packet[col["internal_mapping"]] = self.cast(
                row[col["source_name"]],
                col["data_type"]
            )

        return packet

    def run(self):
        df = pd.read_csv(self.file_path)

        for _, row in df.iterrows():
            packet = self.map_row(row)
            self.queue.put(packet)
            time.sleep(self.delay)