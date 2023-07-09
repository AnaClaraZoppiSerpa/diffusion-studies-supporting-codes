from ga import *
import sys
from time_finder import *

GF2_2 = galois.GF(2 ** 2)
GF2_3 = galois.GF(2 ** 3)
GF2_5 = galois.GF(2 ** 5)
GF2_6 = galois.GF(2 ** 6)
GF2_7 = galois.GF(2 ** 7)
GF2_9 = galois.GF(2 ** 9)
GF2_10 = galois.GF(2 ** 10)
GF2_11 = galois.GF(2 ** 11)
GF2_12 = galois.GF(2 ** 12)
GF2_13 = galois.GF(2 ** 13)
GF2_14 = galois.GF(2 ** 14)
GF2_15 = galois.GF(2 ** 15)
GF2_16 = galois.GF(2 ** 16)

field_order_pairs = [
    (2, GF2_2),
    (3, GF2_3),
    (5, GF2_5),
    (6, GF2_6),
    (7, GF2_7),
    (9, GF2_9),
    (10, GF2_10),
    (11, GF2_11),
    (12, GF2_12),
    (13, GF2_13),
    (14, GF2_14),
    (15, GF2_15),
    (16, GF2_16),
]

# stopped here (11, <class 'galois.GF(2^11)'>, 6).
# maybe re-run this one because it was interrupted when I left the office
# also re-run gf2^13 dim 7 and gf2^14 dim 7, dim 8 gf2^14
def alternative_fields(order, field, dimension):
    E = ExperimentSettings(order=order, dimension=dimension, field=field)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, sys._getframe().f_code.co_name)

function_calls = []

for dim in [2, 3, 4, 5, 6, 7, 8, 16, 32]:
    for (order, field) in field_order_pairs:
        function_calls.append((alternative_fields, order, field, dim))

timed_experiment_with_args(function_calls, 120 * 60)
