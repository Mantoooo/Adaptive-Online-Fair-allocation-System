# 📘 Fair Online Resource Allocation with Multi-Attribute Constraints

## 🚀 Overview

This project focuses on **online resource allocation under fairness constraints** in a **multi-attribute setting**.

In real-world systems such as cloud computing platforms and data centers, jobs arrive sequentially and decisions must be made **without knowledge of future arrivals**. The key challenge is to **maximize efficiency (total value)** while ensuring **fairness across different groups**.

We implement multiple baseline algorithms and propose an **Adaptive FairAllocator** to achieve a strong balance between fairness and efficiency.

---

## 🎯 Problem Statement

- Jobs arrive **one-by-one (online setting)**
- Each job has:
  - **Value** (derived from CPU usage)
  - **Multiple group labels** (priority, type, size)
- System has limited capacity **B**

### Objective:
- Maximize total value  
- Maintain fairness across groups  

---

## ⚖️ Fairness Metric

For each group:

rate(c) = accepted_jobs / total_jobs


### Fairness Gap:

gap = max(rate) - min(rate)


- Lower gap → better fairness  
- Higher value → better efficiency  

---

## 🧠 Algorithms Implemented

### 1. Greedy
- Accepts jobs until capacity is full  
- ❌ Ignores fairness  

---

### 2. D-SETASIDE
- Uses group quotas  
- Ensures minimum fairness  
- ❌ Very strict → low value  

---

### 3. R-SETASIDE
- Adds randomness after quotas  
- Accepts with probability = value / threshold  
- ✔ Better efficiency than D-SETASIDE  

---

### 4. Proportional Fairness (PF)
- Tracks utility per group  
- Prioritizes under-served groups  
- ❌ Complex in multi-attribute settings  

---

### 5. 🔥 Adaptive FairAllocator (Proposed)

- Uses **acceptance rate for fairness**
- Combines value and fairness:

score = α * value + (1 - α) * fairness


- Uses **dynamic threshold**
- Estimates **θ (theta) online**

✔ Simple  
✔ Adaptive  
✔ Interpretable  

---

## ⚙️ Key Concepts

### 🔹 Theta (θ)
- Measures variation in job values

θ = max(value) / min(value)


- Estimated dynamically using a sliding window  

---

### 🔹 Online Setting
- Jobs processed sequentially  
- No knowledge of future jobs  
- Decisions are irreversible  

---

## 📊 Dataset

- Based on **Google Cluster workload traces**
-link -> https://www.kaggle.com/datasets/derrickmwiti/google-2019-cluster-sample
- Extracted:
  - CPU usage → job value  
  - Priority → group  
  - Scheduling class → group  

Additional grouping:
- Small / Large (based on CPU)

---

## 🧪 Experimental Setup

- Jobs processed sequentially  
- Multiple runs with shuffled order  
- Results averaged over runs  

### Parameters:
- Budget (B): configurable  
- Runs: multiple  
- Alpha (α): trade-off parameter  

---

## 📈 Results Summary

| Algorithm        | Value | Fairness |
|-----------------|------|----------|
| Greedy          | Medium | Poor ❌ |
| D-SETASIDE      | Low ❌ | Good ✔ |
| R-SETASIDE      | High ✔ | Moderate |
| PF              | High | Moderate |
| Adaptive        | High ✔ | Good ✔ |

👉 **Adaptive FairAllocator achieves best balance between fairness and efficiency**

---

## 📊 Visualizations

- Value comparison (bar chart)  
- Fairness gap comparison  
- Value vs fairness trade-off  

---

## 🧩 Project Structure

project/
│
├── src/
│ ├── algorithms/
│ │ ├── greedy.py
│ │ ├── dsetaside.py
│ │ ├── rsetaside.py
│ │ ├── pf.py
│ │ └── adaptive.py
│ │
│ ├── allocator.py
│ ├── fairness.py
│ ├── theta.py
│ ├── job.py
│ └── main.py
│
├── data/
│ └── google_cluster_sample.csv
│
└── README.md


---

## ▶️ How to Run

### 1. Install dependencies
pip install pandas matplotlib


### 2. Run the project
python src/main.py


---

## 👥 Team Members

- Utkarsh Agarwal  
- Manan Ashokkumar Solanki  
- Arjun Reju  

---

## 📄 Reference

Fair Online Resource Allocation with Multi-Attribute Constraints  
https://arxiv.org/pdf/2510.21055

---

## 🔮 Future Work

- Dynamic tuning of α  
- Multi-resource allocation (CPU + memory)  
- Theoretical guarantees  
- Real-world deployment  

---

## ⭐ Key Takeaway

Balancing fairness and efficiency in online systems is challenging.  
Adaptive and data-driven approaches provide practical and effective solutions.


