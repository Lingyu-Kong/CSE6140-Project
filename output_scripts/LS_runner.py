import os
import subprocess
import random

# Settings
cutoff = 120 #2 minutes
data_dir = "data"
output_dir = "output"
algorithms = ["LS1", "LS2"]

# Set consistent seed for reproducibility
random.seed(42)

# Collect input files
input_files = sorted(f for f in os.listdir(data_dir) if f.endswith(".in"))
small_inputs = [f for f in input_files if f.startswith("small")]
large_inputs = [f for f in input_files if f.startswith("large")]

# Select 10 random files from each category
selected_small = random.sample(small_inputs, 10)
selected_large = random.sample(large_inputs, 10)

# Generate 40 unique seeds (20 per algorithm)
seeds_ls1 = random.sample(range(1000, 9999), 20)
seeds_ls2 = random.sample(range(1000, 9999), 20)

# Run each selected file with its corresponding seed
for alg, seeds in zip(algorithms, [seeds_ls1, seeds_ls2]):
    print(f"\nRunning {alg}...")
    for i, fname in enumerate(selected_small + selected_large):
        seed = seeds[i]
        name_base = fname[:-3]
        fpath = os.path.join(data_dir, fname)
        sol_file = f"{name_base}{alg}_{cutoff}_{seed}.sol"
        sol_path = os.path.join(output_dir, sol_file)

        if os.path.exists(sol_path):
            print(f"Skipping existing: {sol_file}")
            continue

        print(f"Running {alg} on {fname} with seed {seed}")
        try:
            subprocess.run([
                "python3", "runsolver.py",
                "-inst", fpath,
                "-alg", alg,
                "-time", str(cutoff),
                "-seed", str(seed)
            ], timeout=cutoff + 10)
        except subprocess.TimeoutExpired:
            print(f"Timeout occurred for {fname} with {alg}, seed {seed}")
