from ga import *
import sys
from time_finder import *

dims = [2, 3, 4, 5, 6, 7, 8]
field_order_pairs = [
    (4, GF2_4),
    (8, GF2_8)
]
selection_options = [
    fitness_proportionate_selection,
    #rank_based_selection,
    #stochastic_universal_sampling,
]
pairing_options = [
    random_pairing,
    #sequential_pairing,
    #randomized_sequential_pairing,
    #p_tournament_selection,
    #fitness_proportionate_pairing,
]
crossover_options = [
    midpoint_crossover1,
    #midpoint_crossover2,
    #alternating_crossover,
    #random_points_crossover1,
    #random_points_crossover2,
    #random_points_crossover3,
]
mutation_options = [
    mutation1,
    #mutation2,
    #mutation3,
    #mutation4,
]
replacement_options = [
    generational_replacement,
    #fitness_based_replacement,
]
fitness_options = [
    fitness_4,
    #fitness_3,
]

mutation_probs = [
    #0.0,
    #0.1,
    #0.2,
    0.5,
    #0.7,
    #1.0
]

def parameterized_ga(order, field, dimension, sel, pa, cr, mu, re, fi, mu_p):
    E = ExperimentSettings(order=order, dimension=dimension, field=field)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=10, replacement_num_survivors=10,
                  replacement_tournament_size=10, pairing_tournament_size=10, initial_population_size=40,
                  max_iterations=100, selection_num_parents=20, mutation_prob=mu_p)
    F = ChosenFunctions(initialization_with_existing_solutions, sel, pa,
                        cr, mu, re, fi)
    evolve(E, A, F, sys._getframe().f_code.co_name)

function_calls = []

for dim in dims:
    for order, gf in field_order_pairs:
        for selection_option in selection_options:
            for pairing_option in pairing_options:
                for crossover_option in crossover_options:
                    for mutation_option in mutation_options:
                        for replacement_option in replacement_options:
                            for fitness_option in fitness_options:
                                for mutation_prob in mutation_probs:
                                    function_calls.append((parameterized_ga, order, gf, dim, selection_option, pairing_option, crossover_option, mutation_option, replacement_option, fitness_option, mutation_prob))

timed_experiment_with_args(function_calls, 120 * 60)
