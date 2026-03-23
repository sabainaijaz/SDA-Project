from inspect import signature
from multiprocessing import Queue
from core.functional import verify_signature, filter_verified

class Worker:
    def __init__(self, input_queue: Queue, output_queue: Queue, secret_key: str, iterations: int):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.secret_key = secret_key
        self.iterations = iterations

    def run(self):
        while True:
            try: 
                packet = self.input_queue.get()  # get one packet
                packet = self.input_queue.get()  #get oen packet
                value=packet.get("metric_value")
                signature=packet.get("security_hash")
                if value is None or signature is None:
                    continue #skipping invalid packets
                if verify_signature(value, signature, self.secret_key, self.iterations):
                    self.output_queue.put(packet)
            except Exception as e:
                print(f"Worker module error: {e}") 