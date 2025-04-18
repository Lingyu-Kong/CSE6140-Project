#from typing_extensions import TypedDict
from typing import TypedDict #python 3.8 and higher use typing
'''
Defines the core data structures and type aliases used across all solvers.
Includes MSInput for encapsulating a Set Cover instance (universe, subsets, cutoff, seed),
MSCOuput for returning solution details and trace logs, and a Set alias for readability.
'''
class Set(object):
    def __init__(
        self,
        size: int,
        elements: list[int] | set[int],
    ):
        self.size = size
        self.elements = set(elements)
        
class MSCInput(TypedDict):
    """
    The input of the Minimum Set Cover problem.
    """
    n: int
    m: int
    all_sets: list[Set]
    time_cutoff: float
    random_seed: int
    
class MSCOutput(TypedDict):
    """
    The output of the Minimum Set Cover problem.
    """
    value: int
    set_indices: list[int]
    timestamps: list[float] | None
    quality_trace: list[float] | None