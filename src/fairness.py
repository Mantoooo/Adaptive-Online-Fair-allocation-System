# src/fairness.py

from collections import defaultdict

class FairnessTracker:
    def __init__(self):
        self.accepted = defaultdict(int)
        self.total = defaultdict(int)

    def update(self, job, decision):
        for c in job.labels:
            self.total[c] += 1
            if decision:
                self.accepted[c] += 1

    def get_rate(self, c):
        if self.total[c] == 0:
            return 0
        return self.accepted[c] / self.total[c]