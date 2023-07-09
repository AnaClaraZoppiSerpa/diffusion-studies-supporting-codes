import random

def fitness_proportionate_selection(population, num_parents):
    fitness_sum = sum(candidate.fitness() for candidate in population)
    probabilities = [candidate.fitness() / fitness_sum for candidate in population]
    selected_parents = random.choices(population, probabilities, k=num_parents)
    return selected_parents

def tournament_selection(population, num_parents, tournament_size):
    selected_parents = []
    for _ in range(num_parents):
        tournament_candidates = random.sample(population, tournament_size)
        winner = max(tournament_candidates, key=lambda candidate: candidate.fitness())
        selected_parents.append(winner)
    return selected_parents

def rank_based_selection(population, num_parents):
    sorted_population = sorted(population, key=lambda candidate: candidate.fitness())
    ranks = list(range(1, len(population) + 1))
    probabilities = [rank / sum(ranks) for rank in ranks]
    selected_parents = random.choices(sorted_population, probabilities, k=num_parents)
    return selected_parents

def stochastic_universal_sampling(population, num_parents):
    fitness_sum = sum(candidate.fitness() for candidate in population)
    selection_pointer = random.uniform(0, fitness_sum / num_parents)
    selected_parents = []
    current_sum = population[0].fitness()
    i = 0
    for _ in range(num_parents):
        while current_sum < selection_pointer:
            i += 1
            current_sum += population[i].fitness()
        selected_parents.append(population[i])
        selection_pointer += fitness_sum / num_parents
    return selected_parents

def elitism(population, num_elites):
    sorted_population = sorted(population, key=lambda candidate: candidate.fitness(), reverse=True)
    elites = sorted_population[:num_elites]
    return elites

selection1 = fitness_proportionate_selection
selection2 = tournament_selection
selection3 = rank_based_selection
selection4 = stochastic_universal_sampling
selection5 = elitism

