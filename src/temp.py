
import random
import matplotlib.pyplot as plt
import pandas as pd

from job import Job
from fairness import FairnessTracker
from theta import ThetaEstimator

from algorithms.greedy import GreedyAllocator
from algorithms.dsetaside import DSetAsideAllocator
from algorithms.rsetaside import RSetAsideAllocator
from algorithms.pf import PFAllocator
from algorithms.fair import FairAllocator




def load_jobs_from_csv(path, limit=1000):
    df = pd.read_csv(path)

    # 🔥 ADD THIS LINE HERE
    print("Columns:", df.columns.tolist())

    df = df.head(limit)
    return []

jobs_master = load_jobs_from_csv("data/google_cluster_sample.csv", limit=1000)