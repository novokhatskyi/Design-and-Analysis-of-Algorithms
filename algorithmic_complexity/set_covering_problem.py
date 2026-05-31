# Універсальна множина
U = {1, 2, 3, 4, 5, 6, 7, 8, 9}
S = [
    {1, 2, 3},
    {2, 4, 5},
    {3, 6},
    {4, 5, 7},
    {5, 6, 8, 9},
    {7, 8}
]

def greedy_set_cover(U, S):
    chosen_sets = []
    uncovered_elements = U.copy()
    while uncovered_elements:
        best_subset = max(S, key=lambda subset: len(subset & uncovered_elements))
        chosen_sets.append(best_subset)
        uncovered_elements -= best_subset

    return chosen_sets
solution = greedy_set_cover(U, S)
print("Selected subsets for covering the set U:", solution)
