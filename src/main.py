import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pandas as pd
import ast
from job import Job
from fairness import FairnessTracker
from theta import ThetaEstimator

from algorithms.greedy import GreedyAllocator
from algorithms.dsetaside import DSetAsideAllocator
from algorithms.rsetaside import RSetAsideAllocator
from algorithms.pf import PFAllocator
from algorithms.fair import FairAllocator


# ---------------- LOAD DATASET ----------------
def load_jobs_from_csv(path, limit=1000):
    df = pd.read_csv(path)

    # adjust columns if needed
    df = df[["average_usage", "priority", "scheduling_class"]].dropna()
    df = df.head(limit)

    jobs = []

    for _, row in df.iterrows():
        usage = ast.literal_eval(row["average_usage"])
        value = float(usage["cpus"])
        value = min(value, 1.0)

        labels = {
            f"priority_{int(row['priority'])}",
            f"class_{int(row['scheduling_class'])}"
        }

        if value > 0.5:
            labels.add("large")
        else:
            labels.add("small")

        jobs.append(Job(value, labels))

    return jobs


# ---------------- CORE RUN ----------------
def run(jobs, allocator, theta, fairness):
    total_value = 0

    for job in jobs:
        theta.update(job)
        decision = allocator.decide(job)
        fairness.update(job, decision)

        if decision:
            total_value += job.value

    return total_value


# ---------------- FAIRNESS GAP ----------------
def fairness_gap(fairness):
    if len(fairness.total) == 0:
        return 0

    rates = [fairness.get_rate(c) for c in fairness.total]
    return max(rates) - min(rates)


# ---------------- CONFIG ----------------
B = 20

quotas = {
    "priority_0": 3,
    "priority_1": 3,
    "priority_2": 3,
    "class_0": 3,
    "class_1": 3,
    "small": 3,
    "large": 3
}

algorithms = ["Greedy", "D-SETASIDE", "R-SETASIDE", "PF", "Adaptive"]

results = {algo: {"value": 0, "gap": 0} for algo in algorithms}

runs = 100   


# ---------------- LOAD DATA ----------------
jobs_master = load_jobs_from_csv("data/google_cluster_sample.csv", limit=1000)


# ---------------- EXPERIMENT ----------------
for i in range(runs):
    print(f"\n========== RUN {i+1} ==========\n")

    # shuffle jobs for randomness
    jobs = jobs_master.copy()
    random.shuffle(jobs)

    # -------- GREEDY --------
    theta = ThetaEstimator(W=100)
    fairness = FairnessTracker()
    algo = GreedyAllocator(B)

    value = run(jobs, algo, theta, fairness)
    gap = fairness_gap(fairness)

    print("Greedy:", round(value, 3), "Gap:", round(gap, 3))
    results["Greedy"]["value"] += value
    results["Greedy"]["gap"] += gap


    # -------- D-SETASIDE --------
    theta = ThetaEstimator(W=100)
    fairness = FairnessTracker()

    algo = DSetAsideAllocator(B, quotas, theta)

    value = run(jobs, algo, theta, fairness)
    gap = fairness_gap(fairness)

    print("D-SETASIDE:", round(value, 3), "Gap:", round(gap, 3))
    results["D-SETASIDE"]["value"] += value
    results["D-SETASIDE"]["gap"] += gap


    # -------- R-SETASIDE --------
    theta = ThetaEstimator(W=100)
    fairness = FairnessTracker()

    algo = RSetAsideAllocator(B, quotas, theta)

    value = run(jobs, algo, theta, fairness)
    gap = fairness_gap(fairness)

    print("R-SETASIDE:", round(value, 3), "Gap:", round(gap, 3))
    results["R-SETASIDE"]["value"] += value
    results["R-SETASIDE"]["gap"] += gap


    # -------- PF --------
    theta = ThetaEstimator(W=100)
    fairness = FairnessTracker()

    algo = PFAllocator(B, theta_estimator=theta, beta=0.5)

    value = run(jobs, algo, theta, fairness)
    gap = fairness_gap(fairness)

    print("PF:", round(value, 3), "Gap:", round(gap, 3))
    results["PF"]["value"] += value
    results["PF"]["gap"] += gap


    # -------- ADAPTIVE FAIR (YOUR METHOD) --------
    theta = ThetaEstimator(W=100)
    fairness = FairnessTracker()

    algo = FairAllocator(B, theta_estimator=theta, fairness_tracker=fairness, alpha=0.7)

    value = run(jobs, algo, theta, fairness)
    gap = fairness_gap(fairness)

    print("Adaptive:", round(value, 3), "Gap:", round(gap, 3))
    results["Adaptive"]["value"] += value
    results["Adaptive"]["gap"] += gap


# ---------------- FINAL RESULTS ----------------
print("\n========== FINAL AVERAGE ==========\n")

avg_values = []
avg_gaps = []

for algo in algorithms:
    avg_val = results[algo]["value"] / runs
    avg_gap = results[algo]["gap"] / runs

    avg_values.append(avg_val)
    avg_gaps.append(avg_gap)

    print(f"{algo}: Value = {avg_val:.3f}, Gap = {avg_gap:.3f}")


# ---------------- PLOTS ----------------
x = range(len(algorithms))

# VALUE BAR
plt.figure(figsize=(8, 4))
plt.bar(x, avg_values)
plt.xticks(x, algorithms)
plt.ylabel("Average Value")
plt.title("Value Comparison Across Algorithms")
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("value_plot.png")
plt.close()

# FAIRNESS GAP BAR
plt.figure(figsize=(8, 4))
plt.bar(x, avg_gaps)
plt.xticks(x, algorithms)
plt.ylabel("Fairness Gap")
plt.title("Fairness Comparison Across Algorithms")
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("fairness_plot.png")
plt.close()

# TRADE-OFF SCATTER
plt.figure(figsize=(6, 6))
for i, algo in enumerate(algorithms):
    plt.scatter(avg_values[i], avg_gaps[i])
    plt.text(avg_values[i], avg_gaps[i], algo)

plt.xlabel("Value")
plt.ylabel("Fairness Gap")
plt.title("Value vs Fairness Trade-off")
plt.grid(alpha=0.3)
plt.savefig("tradeoff_plot.png")
plt.close()