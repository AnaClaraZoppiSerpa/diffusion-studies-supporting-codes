import random

def random_pairing(selected_parents, args):
    pairs = []
    # Randomly select pairs of distinct parents
    while len(selected_parents) >= 2:
        parent1 = random.choice(selected_parents)
        selected_parents.remove(parent1)
        parent2 = random.choice(selected_parents)
        selected_parents.remove(parent2)
        pairs.append((parent1, parent2))
    return pairs

def sequential_pairing(selected_parents, args):
    pairs = []
    num_parents = len(selected_parents)
    # Pair adjacent parents in the ordered list
    for i in range(num_parents):
        parent1 = selected_parents[i]
        parent2 = selected_parents[(i + 1) % num_parents]  # Wrap around to the first parent
        pairs.append((parent1, parent2))
    return pairs

def randomized_sequential_pairing(selected_parents, args):
    pairs = []
    num_parents = len(selected_parents)
    # Randomly shuffle the selected parents
    random.shuffle(selected_parents)
    # Pair adjacent parents in the shuffled list
    for i in range(num_parents):
        parent1 = selected_parents[i]
        parent2 = selected_parents[(i + 1) % num_parents]  # Wrap around to the first parent
        pairs.append((parent1, parent2))
    return pairs

def p_tournament_selection(selected_parents, args):
    selected_pairs = []
    while len(selected_parents) >= 2:
        print(len(selected_parents), args.pairing_tournament_size)
        # Randomly select parents for the tournament
        tournament = random.sample(selected_parents, min(args.pairing_tournament_size, len(selected_parents)))
        # Compete in the tournament and select the fitter parent
        parent1 = max(tournament, key=lambda candidate: candidate.fitness())
        tournament.remove(parent1)
        parent2 = max(tournament, key=lambda candidate: candidate.fitness())
        # Remove the selected parents from the pool
        selected_parents.remove(parent1)
        selected_parents.remove(parent2)
        selected_pairs.append((parent1, parent2))
    return selected_pairs

def fitness_proportionate_pairing(selected_parents, args):
    pairs = []
    fitness_sum = sum(candidate.fitness() for candidate in selected_parents)
    num_parents = len(selected_parents)
    # Calculate probabilities for each parent
    probabilities = [candidate.fitness() / fitness_sum for candidate in selected_parents]
    # Pair parents based on their probabilities
    while len(selected_parents) >= 2:
        parent1 = random.choices(selected_parents, probabilities)[0]
        index1 = selected_parents.index(parent1)
        selected_parents.pop(index1)
        probabilities.pop(index1)
        parent2 = random.choices(selected_parents, probabilities)[0]
        index2 = selected_parents.index(parent2)
        selected_parents.pop(index2)
        probabilities.pop(index2)
        pairs.append((parent1, parent2))
    return pairs


pairing1 = random_pairing
pairing2 = sequential_pairing
pairing3 = randomized_sequential_pairing
pairing4 = p_tournament_selection
pairing5 = fitness_proportionate_pairing