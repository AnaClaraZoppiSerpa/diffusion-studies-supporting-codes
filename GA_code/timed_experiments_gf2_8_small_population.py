from ga import *
from time_finder import *
import sys

def dim2_gf2_8():
    E = ExperimentSettings(order=4, dimension=2, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, sys._getframe().f_code.co_name)

def dim3_gf2_8():
    E = ExperimentSettings(order=4, dimension=3, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, sys._getframe().f_code.co_name)

def dim4_gf2_8():
    E = ExperimentSettings(order=4, dimension=4, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, sys._getframe().f_code.co_name)

def dim5_gf2_8():
    E = ExperimentSettings(order=4, dimension=5, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, sys._getframe().f_code.co_name)

def dim6_gf2_8():
    E = ExperimentSettings(order=4, dimension=6, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, sys._getframe().f_code.co_name)

def dim7_gf2_8():
    E = ExperimentSettings(order=4, dimension=7, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, sys._getframe().f_code.co_name)

def dim8_gf2_8():
    E = ExperimentSettings(order=4, dimension=8, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, sys._getframe().f_code.co_name)

def dim16_gf2_8():
    E = ExperimentSettings(order=4, dimension=16, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, sys._getframe().f_code.co_name)

def dim32_gf2_8():
    E = ExperimentSettings(order=4, dimension=32, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, sys._getframe().f_code.co_name)

fs = [dim16_gf2_8, dim32_gf2_8]
timed_experiment(fs, 120 * 60) # 2h max per experiment