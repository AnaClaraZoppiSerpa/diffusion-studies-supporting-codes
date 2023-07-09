import random

def generational_replacement(old_population, offspring, args):
    return offspring

def elitism(old_population, offspring, args):
    elites = sorted(old_population, key=lambda x: x.fitness(), reverse=True)[:args.num_elites]
    new_population = elites + offspring[:len(old_population) - args.num_elites]
    return new_population

def r_tournament_selection(population, offspring, args):
    combined_population = population + offspring
    new_population = []
    while len(new_population) < args.num_survivors:
        tournament = random.sample(combined_population, args.tournament_size)
        winner = max(tournament, key=lambda x: x.fitness())
        new_population.append(winner)
    return new_population

def fitness_based_replacement(old_population, offspring, args):
    combined_population = old_population + offspring
    new_population = sorted(combined_population, key=lambda x: x.fitness(), reverse=True)[:args.num_survivors]
    return new_population

replacement1 = generational_replacement
replacement2 = elitism
replacement3 = r_tournament_selection
replacement4 = fitness_based_replacement
