import random
import copy
import time
from typing_extensions import TypedDict
from commons import MSCInput, MSCOutput, Set

class BnBNode(TypedDict):
    """
    Elemental node of the branch-and-bound tree.
    For each node, we store:
    - The current set of elements covered
    - The current set of sets selected
    """
    elements_covered: set[int]
    sets_selected: list[int]
    
# def greedy_upper_bound(
#     universe: set[int],
#     all_sets: list[set[int]],
# ):
#     """
#     This is a greedy algorithm to find an upper bound for the minimum set cover problem.
#     which should be the minimum number of sets needed to cover all elements by greedy selection.
#     """
#     uncovered_elements = copy.deepcopy(universe)
#     selected_sets = []
#     while uncovered_elements:
#         best_set = None
#         best_covered = 0
#         for i, s in enumerate(all_sets):
#             covered = len(uncovered_elements.intersection(s))
#             if covered > best_covered:
#                 best_set = i
#                 best_covered = covered
#         if best_set is None:
#             # no more sets can cover any uncovered elements, this normally should not happen
#             raise ValueError("No more sets can cover any uncovered elements.")
#         selected_sets.append(best_set)
#         uncovered_elements.difference_update(all_sets[best_set])
#     return selected_sets

def greedy_lower_bound(
    num_selected_sets: int,
    uncovered_elements: set[int],
    remained_sets: list[set[int]],
):
    """
    This is a greedy algorithm to find a lower bound for the minimum set cover problem.
    lower_bound = num_selected_sets + the minimum number of sets needed to cover all remaining elements
    """
    uncovered_copy = copy.deepcopy(uncovered_elements)
    add_selected_sets = []
    add_count = 0
    while uncovered_copy:
        best_set = None
        best_covered = 0
        for i, s in enumerate(remained_sets):
            covered = len(uncovered_copy.intersection(s))
            if covered > best_covered:
                best_set = i
                best_covered = covered
        if best_set is None:
            add_count = float("inf")
            break
        add_selected_sets.append(best_set)
        add_count += 1
        uncovered_copy.difference_update(remained_sets[best_set])
    return num_selected_sets + add_count

def exact_bnb(
    input_data: MSCInput,
):
    random.seed(input_data["random_seed"])
    n = input_data["n"]
    m = input_data["m"]
    all_sets = input_data["all_sets"]
    time_cutoff = input_data["time_cutoff"]
    
    U = set(range(1, n + 1))
    all_sets = [set(s.elements) for s in all_sets]
    
    upper_bound = len(all_sets)
    upper_bound_solution = BnBNode(
        elements_covered=set(U),
        sets_selected=list(range(len(all_sets))),
    )
    
    timestamps = []
    quality_trace = []
    start_time = time.time()
    
    def search(
        node: BnBNode,
    ):
        nonlocal upper_bound_solution, upper_bound, quality_trace, timestamps, start_time
        
        # check if the time limit is reached
        if time.time() - start_time > time_cutoff:
            return
        
        # check if the node is a leaf node, which is all elements are covered
        if node["elements_covered"] >= U:
            if len(node["sets_selected"]) < upper_bound:
                upper_bound = len(node["sets_selected"])
                upper_bound_solution = node
                quality_trace.append(upper_bound)
                timestamps.append(time.time() - start_time)
            return
        
        # compute lower bound
        uncovered_elements = U - node["elements_covered"]
        lower_bound = greedy_lower_bound(
            len(node["sets_selected"]),
            uncovered_elements,
            all_sets,
        )
        if lower_bound > upper_bound:
            return # prune the node
        
        e = next(iter(uncovered_elements))
        for i, s in enumerate(all_sets):
            if e in s and i not in node["sets_selected"]:
                # create a new node
                new_node = copy.deepcopy(node)
                new_node["elements_covered"].update(s)
                new_node["sets_selected"].append(i)
                search(new_node)
    
    # start the search
    initial_node = BnBNode(
        elements_covered=set(),
        sets_selected=[],
    )
    search(initial_node)
    
    # return the result
    set_indices = [i+1 for i in upper_bound_solution["sets_selected"]]
    result = MSCOutput(
        value=upper_bound,
        set_indices=set_indices,
        timestamps=timestamps,
        quality_trace=quality_trace,
    )
    return result