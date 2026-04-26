from allocator import Allocator


class GreedyAllocator(Allocator):
    """
    Greedy Algorithm (Baseline)

    Accepts jobs as long as capacity is available.
    Ignores fairness completely.
    """

    def __init__(self, B):
        super().__init__(B)

    def decide(self, job):

        # if capacity available → accept
        if self.can_accept(job):
            return self.accept(job)

        # otherwise reject
        return self.reject()