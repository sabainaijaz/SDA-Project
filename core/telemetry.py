class PipelineTelemetry:
    def __init__(self, raw_queue, processed_queue):
        self.raw_queue = raw_queue
        self.processed_queue = processed_queue

    def get_status(self):
        return self.raw_queue.qsize(), self.processed_queue.qsize()