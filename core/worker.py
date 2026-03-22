from multiprocessing import Queue
from core.functional import filter_verified

class Worker:
    def __init__(self, input_queue: Queue, output_queue: Queue, secret_key: str, iterations: int):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.secret_key = secret_key
        self.iterations = iterations

    def run(self):
        while True:  
            packet = self.input_queue.get()  
            verified = filter_verified([packet], self.secret_key, self.iterations)
            if verified:
                self.output_queue.put(verified[0])