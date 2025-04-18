# CSE6140-Project
Spring 2025 Final Project of GT-CSE6140

## Environment Setup

We need:
- python>=3.10

## Running the algorithms
In terminal use command: 
python run_solver.py -inst data/test|large|small#.in -alg algname -time # [-seed #]
It will automatically create the required files in the desired format

## Overall Structure
The codebase is organized around a clear separation of concerns and an extensible solver interface. At the core, commons.py defines the data types (MSCInput, MSCOutput, and Set) that every algorithm uses, and io_tools.py provides routines to read problem instances from .in files and write solutions and trace logs to .sol and .trace files. The solver.py module implements a Solver class whose solve() method dispatches to one of the four algorithm implementations—selecting between the exact Branch‑and‑Bound in branch_and_bound.py, the greedy approximation in approxgreedy.py, or the two heuristic local searches in linear_search.py—based on the user’s command‑line arguments. Wrappers in run.py and especially runsolver.py tie everything together, parsing -inst, -alg, -time, and -seed flags, constructing an MSCInput, invoking the solver, and saving both the final solution and any intermediate quality‐over‐time traces. Each algorithm file focuses solely on its search logic and reporting, while the surrounding scripts handle I/O, argument parsing, and batch execution.