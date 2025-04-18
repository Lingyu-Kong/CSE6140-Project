
import os
'''
Command‑line interface for the Set Cover project.  
Parses CLI arguments (`-inst`, `-alg`, `-time`, `-seed`), loads the input file, invokes the selected algorithm, 
and writes out the `.sol` and `.trace` files.
'''
algorithms = ["BnB", "LS1", "LS2"]
    
for algorithm in algorithms:
    os.system(f"python solver.py --algorithm {algorithm} --datasets test")
    
for algorithm in algorithms:
    os.system(f"python solver.py --algorithm {algorithm} --datasets small")
    
for algorithm in algorithms:
    os.system(f"python solver.py --algorithm {algorithm} --datasets large")
    
for algorithm in algorithms:
    os.system(f"python solver.py --algorithm {algorithm} --datasets all")