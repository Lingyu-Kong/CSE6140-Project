from typing_extensions import TypedDict

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