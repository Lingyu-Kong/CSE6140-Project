import os
from typing import Literal
from typing_extensions import TypedDict
from io_tools import(
    load_input,
    load_output,
    write_solution, 
    write_trace,
)
from commons import MSCInput, MSCOutput, Set
from branch_and_bound import exact_bnb

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
            pass
        elif self.algorithm == "LS1":
            pass
        elif self.algorithm == "LS2":
            pass
        else:
            raise ValueError(f"Algorithm {self.algorithm} is not supported.")
        return result # type: ignore[unreachable]
    
    def check_result(self, result: MSCOutput, output_file: str) -> bool:
        """
        Check the result of the solver.
        """
        value, set_indices = load_output(output_file)
        _value, _set_indices = result["value"], result["set_indices"]
        assert _value == value, f"Value {value} is not equal to {_value} for {output_file}."
        return True
        
        
if __name__ == "__main__":
    from tqdm import tqdm
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(dir_path, "data")
    files = os.listdir(data_dir)
    files.sort()
    algorithm = "BnB"
    
    for file in tqdm(files):
        # if not (file.endswith(".in") and "small" in file):
        # if not (file.endswith(".in") and "large" in file):
        if not file.endswith(".in"):
            continue
        input_file = os.path.join(data_dir, file)
        output_file = os.path.join(data_dir, file.replace(".in", ".out"))
        
        solver = MSCSolver(
            input_file=input_file,
            algorithm=algorithm,
            time_cutoff=3600,
            random_seed=42,
        )
        result = solver.solve()
        check_result = solver.check_result(result, output_file)
        assert check_result, f"Result is not correct for {file}."
    