import random
def random_initialization(population_size, upper_bound, rows, cols, args):
    population = []
    for _ in range(population_size):
        matrix = []
        for _ in range(rows):
            row = [random.randint(1, upper_bound) for _ in range(cols)]
            matrix.append(row)
        population.append(matrix)
    return population

def initialization_with_existing_solutions(population_size, upper_bound, rows, cols, args):
    num_existing_solutions = len(args.existing_solutions)
    if num_existing_solutions >= population_size:
        return random.sample(args.existing_solutions, population_size)
    else:
        population = args.existing_solutions.copy()
        remaining_population_size = population_size - num_existing_solutions
        population.extend(random_initialization(remaining_population_size, upper_bound, rows, cols, args))
        return population