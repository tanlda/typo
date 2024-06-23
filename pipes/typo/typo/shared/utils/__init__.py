import time


class Timer:
    elapsed: float = 0.0
    start: float = 0.0
    end: float = 0.0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.elapsed = self.end - self.start
