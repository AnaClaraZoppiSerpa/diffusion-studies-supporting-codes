import random

def reproduction(selected_pairs, mutation_probability, crossover_f, mutation_f, mutation_args):
    offspring = []
    for parent1, parent2 in selected_pairs:
        child1, child2 = crossover_f(parent1.matrix, parent2.matrix)
        if random.random() < mutation_probability:
            child1 = mutation_f(child1, mutation_args)
        if random.random() < mutation_probability:
            child2 = mutation_f(child2, mutation_args)
        offspring.extend([child1, child2])
    return offspring
