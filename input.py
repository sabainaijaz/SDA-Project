import pandas as pd
import time
import hashlib

class Input:
    def __init__(self, config: dict, output_queue):
        self.config = config
        self.queue = output_queue

        # extracting values from config
        self.file_path = config["file"]
        self.schema = config["columns"]
        self.delay = config["speed"]["input_delay"]
        self.secret_key = config["security"]["secret_key"]
        self.iterations = config["security"]["iterations"]

    # returns the correct data type
    def datatype(self, value, data_type):
        try:
            if data_type == "string":
                return str(value)
            elif data_type == "integer":
                return int(value)
            elif data_type == "float":
                return float(value)
            else:
                return value
        except:
            return None   

    # Converts one row to dictionary and calculates hash
    def convertRow(self, row: dict) -> dict:
        mapped = dict(
            map(
                lambda col: (
                    col["to"],
                    self.datatype(row.get(col["from"]), col["type"])
                ),
                self.schema
            )
        )

        # SAFE VALUE EXTRACTION + ROUNDING
        value = mapped.get("metric_value")
        value_str = str(round(value, 2)) if value is not None else "0"

        # CORRECT HASHING (password = key, salt = value)
        mapped["security_hash"] = hashlib.pbkdf2_hmac(
            'sha256',
            self.secret_key.encode('utf-8'),   # password
            value_str.encode('utf-8'),         # salt
            self.iterations
        ).hex()

        return mapped

    # Imperative shell: reads CSV and pushes rows into queue
    def run(self):
        try:
            df = pd.read_csv(self.file_path)

            # Convert all rows
            mapped_rows = list(
                map(
                    lambda r: self.convertRow(r[1].to_dict()),
                    df.iterrows()
                )
            )

            #sends row to worker and pauses for a while so that all rows dont reach at the same time
            list(
                map(
                    lambda row: (self.queue.put(row), time.sleep(self.delay)),
                    mapped_rows
                )
            )

        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except Exception as e:
            print(f"Error in input module: {e}")