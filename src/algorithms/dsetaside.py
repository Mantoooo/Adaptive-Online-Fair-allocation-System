from allocator import Allocator


class DSetAsideAllocator(Allocator):
    """
    Deterministic Set-Aside Algorithm (GFQ)

    Implements:
    1. Reserve quota m_j for each group
    2. After quota satisfied → use threshold λ_i
    """

    def __init__(self, B, quotas, theta_estimator=None):
        super().__init__(B)

        self.quotas = quotas                  # m_j for each group
        self.group_alloc = {g: 0 for g in quotas}

        self.theta_estimator = theta_estimator

    def decide(self, job):

        # ---------------------------
        # Step 0: Capacity check
        # ---------------------------
        if not self.can_accept(job):
            return self.reject()

        # ---------------------------
        # Step 1: Check quota
        # ---------------------------
        for g in job.labels:
            if g in self.quotas and self.group_alloc[g] < self.quotas[g]:
                self._update_groups(job)
                return self.accept(job)

        # ---------------------------
        # Step 2: Threshold decision
        # ---------------------------
        threshold = self._get_threshold(job)

        if job.value >= threshold:
            self._update_groups(job)
            return self.accept(job)

        return self.reject()

    # ---------------------------
    # Threshold function λ_i
    # ---------------------------
    def _get_threshold(self, job):

        # number of accepted jobs so far
        i = self.used

        # estimate theta
        theta = self._get_theta(job)

        # simple increasing threshold
        # λ_i grows from 1 → θ
        threshold = 1 + (i / self.B) * (theta - 1)

        return threshold

    # ---------------------------
    # Get θ (important for your project)
    # ---------------------------
    def _get_theta(self, job):

        if self.theta_estimator is None:
            return 10  # fallback

        # average theta across labels
        values = []

        for g in job.labels:
            t = self.theta_estimator.get_theta(g)
            if t > 0:
                values.append(t)

        if len(values) == 0:
            return 10

        return max(values)

    # ---------------------------
    # Update group allocations
    # ---------------------------
    def _update_groups(self, job):
        for g in job.labels:
            if g in self.group_alloc:
                self.group_alloc[g] += 1