import os
from typing import Literal
#from typing_extensions import TypedDict
from typing import TypedDict #python 3.8 and higher use typing
from io_tools import(
    load_input,
    load_output,
    write_solution, 
    write_trace,
)
from commons import MSCInput, MSCOutput, Set
from branch_and_bound import exact_bnb
from linear_search import annealing_simulate, hill_climbing
from approxgreedy import greedy_set_cover

class MSCSolver:
    """
    The solver of the Minimum Set Cover problem.
    Support multiple algorithms:
    - Exact branch-and-bound
    - Approximation algorithm with approximation guarantees
    - Local search algorithm - Simulated Annealing
    - Local search algorithm - Hill Climbing
    - Local search algorithm - Tabu Search (choose two from all LS algorithms)
    """
    def __init__(
        self,
        input_file: str,
        algorithm: Literal["BnB", "Approx", "LS1", "LS2"],
        time_cutoff: float,
        random_seed: int,
    ):
        
        self.input_file = input_file
        self.algorithm = algorithm
        self.time_cutoff = time_cutoff
        n, m, all_sets = load_input(input_file)
        self.input_data = MSCInput(
            n=n,
            m=m,
            all_sets=all_sets,
            time_cutoff=time_cutoff,
            random_seed=random_seed,
        )
    
    def solve(self) -> MSCOutput:
        """
        Solve the Minimum Set Cover problem.
        """
        if self.algorithm == "BnB":
            result = exact_bnb(self.input_data)
        elif self.algorithm == "Approx":
            result = greedy_set_cover(self.input_data)
        elif self.algorithm == "LS1":
            result = hill_climbing(self.input_data)
        elif self.algorithm == "LS2":
            result = annealing_simulate(self.input_data)
        else:
            raise ValueError(f"Algorithm {self.algorithm} is not supported.")
        return result # type: ignore[unreachable]
    
    def check_result(self, result: MSCOutput, output_file: str) -> bool:
        """
        Check the result of the solver.
        """
        value, set_indices = load_output(output_file)
        _value, _set_indices = result["value"], result["set_indices"]
        if _value != value:
            return False
        else:
            return True
        
        
if __name__ == "__main__":
    from tqdm import tqdm
    import time
    import argparse
    
    parser = argparse.ArgumentParser(description="Minimum Set Cover Solver")
    parser.add_argument("--algorithm", type=str, help="Algorithm to use")
    parser.add_argument("--time_cutoff", type=float, default=300, help="Time cutoff in seconds")
    parser.add_argument("--datasets", type=str, default="all", help="Path to the datasets")
    args = parser.parse_args()
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(dir_path, "data")
    files = os.listdir(data_dir)
    files.sort()
    algorithm = args.algorithm
    
    results = []
    times = []
    time_outs = []
    for file in tqdm(files):
        # if not (file.endswith(".in") and "small" in file):
        # if not (file.endswith(".in") and "large" in file):
        if not file.endswith(".in"):
            continue
        if args.datasets != "all" and args.datasets not in file:
            continue
        input_file = os.path.join(data_dir, file)
        output_file = os.path.join(data_dir, file.replace(".in", ".out"))
        time1 = time.time()
        solver = MSCSolver(
            input_file=input_file,
            algorithm=algorithm,
            time_cutoff=args.time_cutoff,
            random_seed=42,
        )
        time_taken = time.time() - time1
        if time_taken >= args.time_cutoff:
            time_outs.append(1)
        else:
            time_outs.append(0)
        result = solver.solve()
        check_result = solver.check_result(result, output_file)
        results.append(check_result)
        times.append(time_taken)
        
    print("Success Rate: ", sum(results) / len(results))
    print("Timeout Rate: ", sum(time_outs) / len(time_outs))
    print("Average Time: ", sum(times) / len(times))
    
    with open(f"results_{args.datasets}.txt", "a") as f:
        f.write(f"Configs: {args.algorithm}, {args.time_cutoff}, {args.datasets}\n")
        f.write(f"Success Rate: {sum(results) / len(results)}\n")
        f.write(f"Timeout Rate: {sum(time_outs) / len(time_outs)}\n")
        f.write(f"Average Time: {sum(times) / len(times)}\n")
        f.write("==========================================================================\n")
    