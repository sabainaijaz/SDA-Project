class Worker:
    def __init__(self, in_q, out_q, key, iterations):
        self.in_q = in_q
        self.out_q = out_q
        self.key = key
        self.iterations = iterations

    def run(self):
        from core.functional import verify_signature

        while True:
            packet = self.in_q.get()

            if verify_signature(packet, self.key, self.iterations):
                self.out_q.put(packet)