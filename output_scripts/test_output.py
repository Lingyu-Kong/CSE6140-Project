import os
import subprocess

algorithms = ["BnB", "Approx", "LS1", "LS2"]
test_files = sorted(f for f in os.listdir("data") if f.startswith("test") and f.endswith(".in"))
cutoff = 30  # quick runs

for test_file in test_files:
    for alg in algorithms:
        cmd = [
            "python3", "runsolver.py",
            "-inst", os.path.join("data", test_file),
            "-alg", alg,
            "-time", str(cutoff)
        ]
        # Add a seed only for randomized algorithms
        #if alg in ["LS1", "LS2"]:
           # cmd += ["-seed", "1"]

        print(f"\n Running {alg} on {test_file}...")
        subprocess.run(cmd)
