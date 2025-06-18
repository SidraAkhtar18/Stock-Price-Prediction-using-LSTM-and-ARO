import random

def artificial_rabbit_optimization(search_space, objective_fn, n_iter=10):
    best_params = None
    best_score = float('inf')
    for _ in range(n_iter):
        candidate = {key: random.choice(values) for key, values in search_space.items()}
        score = objective_fn(candidate)
        if score < best_score:
            best_score = score
            best_params = candidate  
    return best_params
