from allocator import Allocator
import random


class RSetAsideAllocator(Allocator):
    """
    Randomized Set-Aside Algorithm (GFQ)

    Implements:
    1. Quota-based reservation (same as D-SETASIDE)
    2. Fractional decision
    3. Probabilistic rounding (simulates lossless rounding)
    """

    def __init__(self, B, quotas, theta_estimator=None):
        super().__init__(B)

        self.quotas = quotas
        self.group_alloc = {g: 0 for g in quotas}

        self.theta_estimator = theta_estimator

        # fractional usage tracker (zt in paper)
        self.fractional_used = 0.0

    def decide(self, job):

        # ---------------------------
        # Step 0: Capacity check
        # ---------------------------
        if not self.can_accept(job):
            return self.reject()

        # ---------------------------
        # Step 1: Quota check
        # ---------------------------
        for g in job.labels:
            if g in self.quotas and self.group_alloc[g] < self.quotas[g]:
                self._update_groups(job)
                return self.accept(job)

        # ---------------------------
        # Step 2: Fractional decision
        # ---------------------------
        threshold = self._get_threshold(job)

        # fractional allocation x̃t ∈ [0,1]
        frac = min(1.0, job.value / threshold)

        # update fractional usage
        prev_used = self.fractional_used
        self.fractional_used += frac

        # ---------------------------
        # Step 3: Rounding
        # ---------------------------
        accept = self._round(frac, prev_used)

        if accept:
            self._update_groups(job)
            return self.accept(job)

        return self.reject()

    # ---------------------------
    # Threshold function
    # ---------------------------
    def _get_threshold(self, job):

        i = self.used
        theta = self._get_theta(job)

        return 1 + (i / self.B) * (theta - 1)

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

    # ---------------------------
    # Rounding function (simplified)
    # ---------------------------
    def _round(self, frac, prev_used):

        # probabilistic rounding
        # accept with probability = frac
        return random.random() < frac

    # ---------------------------
    # Update group allocations
    # ---------------------------
    def _update_groups(self, job):
        for g in job.labels:
            if g in self.group_alloc:
                self.group_alloc[g] += 1