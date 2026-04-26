# src/job.py

class Job:
    def __init__(self, value, labels):
        self.value = value        # CPU request (normalized)
        self.labels = labels      # set of class IDs

    def __repr__(self):
        return f"Job(value={self.value}, labels={self.labels})"