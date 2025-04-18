
from commons import MSCInput, MSCOutput, Set
# Approximation algorithm using a greedy approach to solve the Minimum Set Cover Problem
# At each step we pick the subset that covers the most currently uncovered elements
# until all elements are covered
def greedy_set_cover(input_data: MSCInput) -> MSCOutput:
    n = input_data["n"]
    m = input_data["m"]
    all_sets = input_data["all_sets"]
    
    universe = set(range(1, n + 1)) # Set of possible numbers
    covered = set() # Set containing the numbers already covered in a set (initially empty)
    selected_subsets = [] # Set containing the indices of the sets covered (initially empty)
    used = set()  # Set containing used subset indices (initially empty)

    while covered != universe: 
        best_subset_index = -1 # Reset the index for each round
        best_subset_new_coverage = set() # To maintain the best subset coverage for each round

        for i in range(m):
            # Going through all unused sets to determine the one with better coverage (more uncovered numbers)
            if i in used:
                continue  # Skip sets already used
            subset = all_sets[i].elements # Get the numbers in the set i
            new_coverage = subset - covered # Select only those not already covered

            if len(new_coverage) > len(best_subset_new_coverage): 
                # Update best coverage if more numbers covered in this set than in any previous 
                best_subset_index = i
                best_subset_new_coverage = new_coverage

        if best_subset_index == -1:
            break  # No more progress possible 

        covered.update(best_subset_new_coverage) # Add newly covered numbers
        selected_subsets.append(best_subset_index + 1) # Add the index of the subset selected
        used.add(best_subset_index) # Mark the subset as used
    selected_subsets = sorted(i+1 for i in selected_subsets)
    return MSCOutput(
        value=len(selected_subsets),
        set_indices=selected_subsets,
        timestamps=None,
        quality_trace=None,
    )

