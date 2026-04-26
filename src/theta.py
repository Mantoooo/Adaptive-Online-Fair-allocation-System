from collections import defaultdict

class ThetaEstimator:
    """
    Sliding Window Theta Estimator

    θ_j = max(value) / min(value) over last W jobs of class j
    """

    def __init__(self, W=100):
        self.W = W
        self.history = defaultdict(list)

    def update(self, job):
        for c in job.labels:
            self.history[c].append(job.value)

            # keep sliding window
            if len(self.history[c]) > self.W:
                self.history[c].pop(0)

    def get_theta(self, c):
        vals = self.history[c]

        if len(vals) < 2:
            return 1.0  # cold start

        min_val = min(vals)

        # avoid division by zero
        if min_val <= 1e-6:
            return max(vals)

        return max(vals) / min_val