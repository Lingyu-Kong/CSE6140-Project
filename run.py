import os

algorithms = ["BnB", "LS1", "LS2"]
    
for algorithm in algorithms:
    os.system(f"python solver.py --algorithm {algorithm} --datasets test")
    
for algorithm in algorithms:
    os.system(f"python solver.py --algorithm {algorithm} --datasets small")
    
for algorithm in algorithms:
    os.system(f"python solver.py --algorithm {algorithm} --datasets large")
    
for algorithm in algorithms:
    os.system(f"python solver.py --algorithm {algorithm} --datasets all")