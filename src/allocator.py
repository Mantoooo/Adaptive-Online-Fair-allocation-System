# src/allocator.py

class Allocator:
    def __init__(self, B):
        self.B = B          # total budget
        self.used = 0       # used capacity

    def can_accept(self, job):
        return self.used < self.B

    def accept(self, job):
        self.used += 1
        return 1

    def reject(self):
        return 0