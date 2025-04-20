import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import glob 

# Configuration
DATA_DIR = "data"
OUT_DIR = "output"
INSTANCES = ["large1", "large10"]
ALGORITHMS = ["LS1", "LS2"]
CUTOFF = 120  # seconds

# Load optimal values
optimal = {}
for inst in INSTANCES:
    out_path = os.path.join(DATA_DIR, f"{inst}.out")
    try:
        with open(out_path) as f:
            optimal[inst] = int(f.readline().strip())
    except FileNotFoundError:
        optimal[inst] = None

# Parse trace files: trace_data[inst][alg] = list of arrays [[t1,q1], [t2,q2], ...] per run
trace_data = {inst: {alg: [] for alg in ALGORITHMS} for inst in INSTANCES}
for inst in INSTANCES:
    for alg in ALGORITHMS:
        pattern = os.path.join(OUT_DIR, f"{inst}_{alg}_{CUTOFF}_*.trace")
        for path in glob.glob(pattern):
            data = np.loadtxt(path, delimiter=None)
            if data.ndim == 1:
                data = data.reshape(1, -1)
            trace_data[inst][alg].append(data)


# 1) Qualified Runtime Distribution (QRTD)
def plot_QRTD(inst, q_stars=[0.0, 0.01, 0.02, 0.05]):
    """
    Qualified Runtime Distribution (QRTD): For each algorithm and q*, 
    show fraction of runs that achieve solution quality ≤ (1 + q*) * OPT by time t.
    """
    opt = optimal[inst]
    times = np.linspace(0, CUTOFF, 100)

    plt.figure(figsize=(8, 6))

    for alg in ALGORITHMS:
        runs = trace_data[inst][alg]
        print(f"[DEBUG] {inst} {alg} has {len(runs)} runs")
        for q_star in q_stars:
            threshold = opt * (1 + q_star)
            fractions = []

            for t in times:
                count = 0
                for run in runs:
                    idx = np.searchsorted(run[:, 0], t, side='right') - 1
                    if idx >= 0:
                        if run[idx, 1] <= threshold:
                            count += 1
                frac = count / len(runs) if runs else 0
                fractions.append(frac)

            plt.step(times, fractions, where='post', label=f"{alg}, q*={q_star:.1%}")

    plt.xlabel("Run-time (s)")
    plt.ylabel("Fraction of runs ≤ quality threshold")
    plt.title(f"Qualified Runtime Distribution for {inst}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 2) Solution Quality Distribution (SQD)
def plot_SQD(inst, time_points=[30, 60, 120]):
    """
    Plots histograms of relative errors for each algorithm at fixed time points.
    Each (alg, t) pair gets its own histogram.
    """
    plt.figure(figsize=(8, 6))
    opt = optimal[inst]

    for alg in ALGORITHMS:
        for t in time_points:
            relerrs = []
            for run in trace_data[inst][alg]:
                idx = np.searchsorted(run[:, 0], t, side='right') - 1
                if idx >= 0 and opt:
                    sol_size = run[idx, 1]
                    relerrs.append((sol_size - opt) / opt)
            if relerrs:
                plt.hist(relerrs, bins=20, alpha=0.5, label=f"{alg}, t={t}s")

    plt.xlabel("Relative Error")
    plt.ylabel("Frequency")
    plt.title(f"SQD for {inst}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 3) Box plot of last-improvement times
def plot_box(inst):
    """
    Vertical box plot of last-improvement times for each algorithm.
    """
    data = []
    labels = []
    for alg in ALGORITHMS:
        runs = trace_data[inst][alg]
        last_times = [run[-1, 0] for run in runs if run.size > 0]
        if last_times:
            data.append(last_times)
            labels.append(alg)
    if not data:
        print(f"No data for {inst}")
        return
    plt.figure(figsize=(6, 6))
    plt.boxplot(
        data,
        labels=labels,
        vert=True,
        widths=0.6,
        boxprops=dict(linewidth=2),
        whiskerprops=dict(linewidth=2),
        capprops=dict(linewidth=2),
        medianprops=dict(linewidth=2)
    )
    plt.xlabel("Algorithm")
    plt.ylabel("Time of last improvement (s)")
    plt.title(f"Last Improvement Times for {inst}")
    plt.tight_layout()
    plt.show()

# Generate plots for each instance
for inst in INSTANCES:
    plot_QRTD(inst)
    plot_SQD(inst)
    plot_box(inst)
