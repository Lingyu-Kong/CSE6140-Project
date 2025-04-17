import time
import random
import math
import copy
from commons import MSCInput, MSCOutput, Set

MAX_ITER = 1000_000  # maximum iterations

def cost_function(
    selected_sets: list[int],
    all_sets: list[set[int]],
    U: set[int],
    penalty_factor: float,
) -> float:
    """
    Calculate the cost of the current solution.
    The cost is the number of uncovered elements.
    """
    uncovered_elements = U.copy()
    for i in selected_sets:
        uncovered_elements.difference_update(all_sets[i])
    return len(uncovered_elements) * penalty_factor + len(selected_sets)

def get_neighbor_solution(
    selected_sets: list[int],
    all_sets: list[set[int]],
) -> list[int]:
    """
    Get a neighbor solution by randomly adding, removing, or replacing a set.
    """
    new_solution = selected_sets.copy()
    if len(new_solution) == 0:
        # if the current solution is empty, add a random set
        candidate_sets = list(set(range(len(all_sets))) - set(new_solution))
        if candidate_sets:
            new_solution.append(random.choice(candidate_sets))
        return new_solution
    elif len(new_solution) == len(all_sets):
        # if the current solution covers all sets, remove a random set
        new_solution.remove(random.choice(new_solution))
        return new_solution
    else:
        if random.random() < 1/3:
            # remove a random set
            new_solution.remove(random.choice(new_solution))
        elif random.random() < 2/3:
            # add a random set
            candidate_sets = list(set(range(len(all_sets))) - set(new_solution))
            if candidate_sets:
                new_solution.append(random.choice(candidate_sets))
        else:
            # replace a random set with another random set
            candidate_sets = list(set(range(len(all_sets))) - set(new_solution))
            if candidate_sets:
                new_solution.remove(random.choice(new_solution))
                new_solution.append(random.choice(candidate_sets))
    return new_solution

def check_solution(
    selected_sets: list[int],
    all_sets: list[set[int]],
    U: set[int],
) -> bool:
    """
    Check if the selected sets cover all elements in the universe.
    """
    covered_elements = set()
    for i in selected_sets:
        covered_elements.update(all_sets[i])
    return len(U.difference(covered_elements)) == 0

def greedy_initial_solution(
    all_sets: list[set[int]],
    U: set[int],
) -> list[int]:
    """
    Generate an initial solution using a greedy algorithm.
    """
    uncovered_elements = U.copy()
    selected_sets = []
    
    while uncovered_elements:
        best_set = None
        best_covered = 0
        for i, s in enumerate(all_sets):
            covered = len(uncovered_elements.intersection(s))
            if covered > best_covered:
                best_set = i
                best_covered = covered
        if best_set is None:
            break
        selected_sets.append(best_set)
        uncovered_elements.difference_update(all_sets[best_set])
    
    return selected_sets

def allcover_initial_solution(
    all_sets: list[set[int]],
    U: set[int],
) -> list[int]:
    """
    Generate an initial solution by including all sets.
    """
    selected_sets = list(range(len(all_sets)))
    uncovered_elements = set()
    
    for i in selected_sets:
        uncovered_elements.update(all_sets[i])
    
    if len(uncovered_elements) == 0:
        return selected_sets
    else:
        return []

def annealing_simulate(
    input_data: MSCInput,
) -> MSCOutput:
    """
    Solve the Minimum Set Cover problem using simulated annealing.
    """
    random.seed(input_data["random_seed"])
    n = input_data["n"]
    m = input_data["m"]
    all_sets = input_data["all_sets"]
    time_cutoff = input_data["time_cutoff"]
    
    U = set(range(1, n + 1))
    all_sets = [set(s.elements) for s in all_sets]
    
    T0 = 100.0       # initial temperature
    T1 = 1        # final temperature
    ALPHA = T1 / T0  # cooling rate
    PENALTY_FACTOR = n + 1  # penalty factor for uncovered elements
    
    timestamps = []
    quality_trace = []
    start_time = time.time()
    current_solution = greedy_initial_solution(all_sets, U)
    current_cost = cost_function(current_solution, all_sets, U, PENALTY_FACTOR)
    timestamps.append(time.time() - start_time)
    quality_trace.append(current_cost)
    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost
    T = T0
    for iter_id in range(MAX_ITER):
        if time.time() - start_time > time_cutoff:
            break
        new_solution = get_neighbor_solution(current_solution, all_sets)
        new_cost = cost_function(new_solution, all_sets, U, PENALTY_FACTOR)
        delta = new_cost - current_cost
        if delta <= 0:
            # if the new solution is better, accept it
            current_solution = new_solution
            current_cost = new_cost
        else:
            # even if the new solution is worse, accept it with a probability
            # based on e^(-delta / T)
            if random.random() < math.exp(-delta / T):
                current_solution = new_solution
                current_cost = new_cost
        
        # update the best solution
        if current_cost < best_cost and check_solution(current_solution, all_sets, U):
            best_solution = current_solution
            best_cost = current_cost
            timestamps.append(time.time() - start_time)
            quality_trace.append(best_cost)
        
        T = T0 * (ALPHA ** (iter_id / MAX_ITER))
    best_solution = sorted(i+1 for i in best_solution) # So we have sets starting from 1 not 0  
    return MSCOutput(
        value=len(best_solution),
        set_indices=best_solution,
        timestamps=timestamps,
        quality_trace=quality_trace,
    )
    

def hill_climbing(
    input_data: MSCInput,
) -> MSCOutput:
    """
    Solve the Minimum Set Cover problem using hill climbing.
    """
    random.seed(input_data["random_seed"])
    n = input_data["n"]
    m = input_data["m"]
    all_sets = input_data["all_sets"]
    time_cutoff = input_data["time_cutoff"]
    
    U = set(range(1, n + 1))
    all_sets = [set(s.elements) for s in all_sets]
    
    PENALTY_FACTOR = n + 1  # penalty factor for uncovered elements
    
    start_time = time.time()
    timestamps = []
    quality_trace = []
    current_solution = greedy_initial_solution(all_sets, U)
    current_cost = cost_function(current_solution, all_sets, U, PENALTY_FACTOR)
    timestamps.append(time.time() - start_time)
    quality_trace.append(current_cost)
    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost
    
    for iter_id in range(MAX_ITER):
        if time.time() - start_time > time_cutoff:
            break
        new_solution = get_neighbor_solution(current_solution, all_sets)
        new_cost = cost_function(new_solution, all_sets, U, PENALTY_FACTOR)
        if new_cost <= current_cost:
            current_solution = new_solution
            current_cost = new_cost
            if current_cost < best_cost and check_solution(current_solution, all_sets, U):
                best_solution = current_solution
                best_cost = current_cost
                timestamps.append(time.time() - start_time)
                quality_trace.append(best_cost)
    best_solution = sorted(i+1 for i in best_solution) # So we have sets starting from 1 not 0
    return MSCOutput(
        value=len(best_solution),
        set_indices=best_solution,
        timestamps=timestamps,
        quality_trace=quality_trace,
    )