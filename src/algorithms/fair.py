# from allocator import Allocator

# class FairAllocator(Allocator):
#     def __init__(self, B, theta, fairness, epsilon=1.0, warmup_ratio=0.1, gap_tol=0.02, value_tol=0.2):
#         super().__init__(B)
#         self.theta = theta
#         self.fairness = fairness
#         self.epsilon = epsilon
#         self.warmup_ratio = warmup_ratio
#         self.gap_tol = gap_tol
#         self.value_tol = value_tol

#     def decide(self, job):

#         if not self.can_accept(job):
#             return self.reject()

#         # warm start
#         if self.used < 0.1 * self.B:
#             return self.accept(job)

#         if len(self.fairness.total) == 0:
#             return self.accept(job)

#         rates = [self.fairness.get_rate(c) for c in self.fairness.total]
#         avg_rate = sum(rates) / len(rates)

#         help_score = 0
#         hurt_score = 0

#         for c in job.labels:
#             rate = self.fairness.get_rate(c)

#             if rate < avg_rate:
#                 help_score += (avg_rate - rate)
#             else:
#                 hurt_score += (rate - avg_rate)

#         help_score /= len(job.labels)
#         hurt_score /= len(job.labels)

#         # ---------------- STRICT BALANCE ----------------

#         # strongly help under-represented groups
#         if help_score > 0.02 and job.value >= 0.3:
#             return self.accept(job)

#         # allow high value ONLY if fairness is safe
#         if job.value >= 0.75 and hurt_score < 0.015:
#             return self.accept(job)

#         # reject if contributing to unfairness
#         if hurt_score > 0.04:
#             return self.reject()

#         return self.reject()


from allocator import Allocator


class FairAllocator(Allocator):
    """
    Adaptive Fairness Algorithm (Your Contribution)

    Dynamically adjusts allocation based on group imbalance
    """

    def __init__(self, B, theta_estimator=None, fairness_tracker=None, alpha=0.7):
        super().__init__(B)

        self.theta_estimator = theta_estimator
        self.fairness = fairness_tracker

        self.alpha = alpha  # tradeoff: value vs fairness

    def decide(self, job):

        # ---------------------------
        # Step 0: capacity check
        # ---------------------------
        if not self.can_accept(job):
            return self.reject()

        # ---------------------------
        # Step 1: compute fairness score
        # ---------------------------
        fairness_score = self._fairness_score(job)

        # ---------------------------
        # Step 2: combine with value
        # ---------------------------
        combined_score = (
            self.alpha * job.value +
            (1 - self.alpha) * fairness_score
        )

        # ---------------------------
        # Step 3: threshold decision
        # ---------------------------
        threshold = self._get_threshold(job)

        if combined_score >= threshold:
            return self.accept(job)

        return self.reject()

    # ---------------------------
    # Fairness score
    # ---------------------------
    def _fairness_score(self, job):
        if self.fairness is None or len(self.fairness.total) == 0:
            return 0.5
    
        scores = []
    
        for g in job.labels:
            rate = self.fairness.get_rate(g)
            scores.append((1 - rate) * 0.3)   # reduced impact
    
        return sum(scores) / len(scores)

    # ---------------------------
    # Threshold (uses theta)
    # ---------------------------
    def _get_threshold(self, job):

        i = self.used
        theta = self._get_theta(job)

        return 0.2 + (i / self.B) * (theta - 1) * 0.3

    # ---------------------------
    # Theta estimation
    # ---------------------------
    def _get_theta(self, job):

        if self.theta_estimator is None:
            return 10

        values = []

        for g in job.labels:
            t = self.theta_estimator.get_theta(g)
            if t > 0:
                values.append(t)

        if not values:
            return 10

        return max(values)