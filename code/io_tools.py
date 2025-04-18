import os
from commons import Set
'''
Provides helper functions for reading and writing Set Cover instance and solution files.  
Includes routines to parse `.in` input files and to format and output `.sol` and `.trace` files consistently across all algorithms.
'''
def load_input(file_path: str):
    """
    Load input from a .in file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    n, m = 0, 0
    all_sets: list[Set] = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].split(" ")[0])
        m = int(lines[0].split(" ")[1])
        for line in lines[1:]:
            size = int(line.split(" ")[0])
            elements = list(map(int, line.split(" ")[1:]))
            all_sets.append(Set(size, elements))
    return n, m, all_sets

def load_output(file_path: str):
    """
    Load output from a .out file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) == 1:
            value = int(lines[0])
            return value, None
        elif len(lines) == 2:
            value = int(lines[0])
            set_indices = list(map(int, lines[1].split(" ")))
            return value, set_indices
        else:
            raise ValueError(f"Output file {file_path} is not in the correct format.")
        
def write_solution(file_path: str, value: int, set_indices: list[int]):
    """
    Write solution to a .out file
    """
    with open(file_path, 'w') as file:
        file.write(f"{value}\n")
        if set_indices is not None:
            file.write(" ".join(map(str, set_indices)) + "\n")
            
def write_trace(file_path: str, timestamps: list[float], quality_trace: list[float]):
    """
    Write trace to a .trace file
    """
    assert len(timestamps) == len(quality_trace), "Timestamps and quality trace must have the same length."
    with open(file_path, 'w') as file:
        for timestamp, quality in zip(timestamps, quality_trace):
            file.write(f"{timestamp} {quality}\n")