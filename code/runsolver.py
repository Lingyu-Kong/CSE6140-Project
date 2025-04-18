import sys
import os
from solver import MSCSolver
from io_tools import write_solution, write_trace 

"""
Command‑line entrypoint that parses arguments for instance file, algorithm choice, cutoff time, and seed.  
Loads the input via io_tools, dispatches to solver.solve(), and writes out the `.sol` and `.trace` outputs.
"""

output_dir = os.path.join(os.getcwd(), "output") # We redirect our outputs to another folder

def main():
    if len(sys.argv) not in [7, 9]: # We only have 7 inputs if no seed needed
        print("Usage: python run_solver.py -inst <filename> -alg <method> -time <cutoff> [-seed <random_seed>]")
        return

    # We parse the arguments
    args = dict(zip(sys.argv[1::2], sys.argv[2::2])) # We create a dictionary where the key is the flag
    filename = args["-inst"] # We access the file through its flag
    method = args["-alg"] # We access the algorithm through its flag
    cutoff = float(args["-time"]) # Same for time
    seed = int(args.get("-seed", 0))  # Same for the seed, optional for deterministic

    # Solve
    solver = MSCSolver(
        input_file=filename,
        algorithm=method,
        time_cutoff=cutoff,
        random_seed=seed
    )
    result = solver.solve()

    # Get name for the file
    instance = os.path.basename(filename).replace(".in", "")

    # Create solution file name
    if method == "Approx" or method == "BnB" or method == "LS2":
        # We do not need a seed for this methods 
        output_filename = os.path.join(output_dir, f"{instance}_{method}_{int(cutoff)}.sol")
    else:
        # We only use it for LS1
        output_filename = os.path.join(output_dir, f"{instance}_{method}_{int(cutoff)}_{seed}.sol")

    # We write the first file .sol
    write_solution(output_filename, result["value"], result["set_indices"])

    # Write the second file .trace if required
    if method != "Approx":
        trace_filename = output_filename.replace(".sol", ".trace")
        write_trace(trace_filename, result["timestamps"], result["quality_trace"])

    print(f"Solution written to {output_filename}")
    if method != "Approx":
        print(f"Trace written to {trace_filename}")

if __name__ == "__main__":
    main()
