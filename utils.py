import numpy as np
from individual import Individual

# Fast non-dominated sort
def fast_non_dominated_sort(population):
    fronts = [[]]
    for p in population:
        p.dominated_solutions = []
        p.domination_count = 0
        for q in population:
            if dominates(p, q):
                p.dominated_solutions.append(q)
            elif dominates(q, p):
                p.domination_count += 1
        if p.domination_count == 0:
            p.rank = 0
            fronts[0].append(p)
    i = 0
    while len(fronts[i]) > 0:
        next_front = []
        for p in fronts[i]:
            for q in p.dominated_solutions:
                q.domination_count -= 1
                if q.domination_count == 0:
                    q.rank = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    return fronts[:-1]

def dominates(p, q):
    better_in_all = all(p_i <= q_i for p_i, q_i in zip(p.objectives, q.objectives))
    better_in_one = any(p_i < q_i for p_i, q_i in zip(p.objectives, q.objectives))
    return better_in_all and better_in_one

def calculate_crowding_distance(front):
    n_objectives = len(front[0].objectives)
    for ind in front:
        ind.crowding_distance = 0.0
    for m in range(n_objectives):
        front.sort(key=lambda x: x.objectives[m])
        front[0].crowding_distance = front[-1].crowding_distance = float('inf')
        m_values = [ind.objectives[m] for ind in front]
        min_m = min(m_values)
        max_m = max(m_values)
        if max_m == min_m:
            continue
        for i in range(1, len(front) - 1):
            front[i].crowding_distance += (front[i+1].objectives[m] - front[i-1].objectives[m]) / (max_m - min_m)
