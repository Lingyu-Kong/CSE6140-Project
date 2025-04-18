import os
import subprocess

# Settings
cutoff = 600  # 10 minutes
data_dir = "data"
output_dir = "output"

# Gather all input files that start with small# or large#
input_files = sorted(
    f for f in os.listdir(data_dir)
    if (f.startswith("small") or f.startswith("large")) and f.endswith(".in")
)

for fname in input_files:
    fpath = os.path.join(data_dir, fname)
    name_base = fname[:-3]  # e.g., small1.in -> small1

    sol_file = f"{name_base}BnB_{cutoff}.sol"
    sol_path = os.path.join(output_dir, sol_file)

    if os.path.exists(sol_path):
        print(f"Skipping existing: {sol_file}")
        continue

    print(f"Running BnB on {fname} for {cutoff} seconds")
    try:
        subprocess.run([
            "python3", "runsolver.py",
            "-inst", fpath,
            "-alg", "BnB",
            "-time", str(cutoff)
        ], timeout=cutoff + 10)
    except subprocess.TimeoutExpired:
        print(f"Timeout occurred while running BnB on {fname}")
