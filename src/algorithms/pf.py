from allocator import Allocator


class PFAllocator(Allocator):
    """
    Proportional Fairness (β-PF inspired)

    Idea:
    Allocate more to under-served groups (low utility)
    """

    def __init__(self, B, theta_estimator=None, beta=0.5):
        super().__init__(B)

        self.theta_estimator = theta_estimator
        self.beta = beta  # fairness vs efficiency tradeoff

        # utility per group U_j
        self.group_utility = {}

    def decide(self, job):

        # ---------------------------
        # Step 0: capacity check
        # ---------------------------
        if not self.can_accept(job):
            return self.reject()

        # ---------------------------
        # Step 1: compute fairness score
        # ---------------------------
        score = self._compute_score(job)

        # ---------------------------
        # Step 2: threshold decision
        # ---------------------------
        threshold = self._get_threshold(job)

        if score >= threshold:
            self._update_utility(job)
            return self.accept(job)

        return self.reject()

    # ---------------------------
    # Fairness-aware score
    # ---------------------------
    def _compute_score(self, job):

        # average utility of job's groups
        utilities = []

        for g in job.labels:
            utilities.append(self.group_utility.get(g, 0))

        avg_utility = sum(utilities) / len(utilities) if utilities else 0

        # fairness adjustment
        # lower utility → higher score
        score = job.value / (1 + avg_utility)

        return score

    # ---------------------------
    # Threshold function
    # ---------------------------
    def _get_threshold(self, job):

        i = self.used
        theta = self._get_theta(job)

        # tradeoff using beta
        base = 1 + (i / self.B) * (theta - 1)

        return 0.1 + self.beta * base * 0.3

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
    # Update utilities
    # ---------------------------
    def _update_utility(self, job):

        for g in job.labels:
            self.group_utility[g] = self.group_utility.get(g, 0) + job.value