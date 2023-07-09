from ga import *

def experiment1():
    # 2x2 matrices, first configuration, 100 iterations
    # I want to see how many MDS matrices we can find, even though they will be worse than the baseline.
    E = ExperimentSettings(
        order=4,
        dimension=2,
        field=GF2_4)
    A = Arguments(
        upper=E.integer_upper_limit,
        replacement_num_elites=None,
        replacement_num_survivors=None,
        replacement_tournament_size=None,
        pairing_tournament_size=None,
        initial_population_size=12,
        max_iterations=500,
        selection_num_parents=6,
        mutation_prob=0.1)
    F = ChosenFunctions(random_initialization,
                        fitness_proportionate_selection,
                        sequential_pairing,
                        random_points_crossover1,
                        mutation1,
                        generational_replacement)
    evolve(E, A, F, "experiment1()")

def experiment2():
    E = ExperimentSettings(
        order=4,
        dimension=3,
        field=GF2_4)
    A = Arguments(
        upper=E.integer_upper_limit,
        replacement_num_elites=None,
        replacement_num_survivors=None,
        replacement_tournament_size=None,
        pairing_tournament_size=None,
        initial_population_size=24,
        max_iterations=300,
        selection_num_parents=12,
        mutation_prob=0.2)
    F = ChosenFunctions(random_initialization,
                        fitness_proportionate_selection,
                        sequential_pairing,
                        random_points_crossover1,
                        mutation1,
                        generational_replacement)
    evolve(E, A, F, "experiment1()")

def experiment3():
    # Using fitness 0 for mds matrices, and fitness_based_replacement
    E = ExperimentSettings(
        order=4,
        dimension=3,
        field=GF2_4)
    A = Arguments(
        upper=E.integer_upper_limit,
        replacement_num_elites=None,
        replacement_num_survivors=24,
        replacement_tournament_size=None,
        pairing_tournament_size=None,
        initial_population_size=24,
        max_iterations=5,
        selection_num_parents=12,
        mutation_prob=0.2)
    F = ChosenFunctions(random_initialization,
                        fitness_proportionate_selection,
                        sequential_pairing,
                        random_points_crossover1,
                        mutation1,
                        fitness_based_replacement,
                        fitness_2)
    evolve(E, A, F, "experiment3()")

def experiment4():
    # Using fitness 0 for mds matrices, and fitness_based_replacement
    E = ExperimentSettings(
        order=4,
        dimension=3,
        field=GF2_4)
    A = Arguments(
        upper=E.integer_upper_limit,
        replacement_num_elites=None,
        replacement_num_survivors=24,
        replacement_tournament_size=None,
        pairing_tournament_size=None,
        initial_population_size=24,
        max_iterations=5,
        selection_num_parents=12,
        mutation_prob=0.2)
    F = ChosenFunctions(random_initialization,
                        fitness_proportionate_selection,
                        sequential_pairing,
                        random_points_crossover1,
                        mutation1,
                        fitness_based_replacement,
                        fitness_1)
    evolve(E, A, F, "experiment3()")

def experiment5(): # Worked well for dim=2,3,4, got stuck for dim=5 with no mds matrices
    E = ExperimentSettings(order=4, dimension=2, field=GF2_4)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=80, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=240,
                  max_iterations=100, selection_num_parents=120, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, "experiment5()")
def experiment6(): #dim=6 requires around 9 minutes.
    E = ExperimentSettings(order=8, dimension=7, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, "testing_dim_7_time")

def experiment7(): #dim=6 requires around 9 minutes.
    E = ExperimentSettings(order=8, dimension=8, field=GF2_8)
    A = Arguments(upper=E.integer_upper_limit, replacement_num_elites=8, replacement_num_survivors=None,
                  replacement_tournament_size=None, pairing_tournament_size=None, initial_population_size=24,
                  max_iterations=100, selection_num_parents=12, mutation_prob=0.5)
    F = ChosenFunctions(random_initialization, rank_based_selection, sequential_pairing,
                        alternating_crossover, mutation4, generational_replacement, fitness_2)
    evolve(E, A, F, "testing_dim_8_time")

experiment6()
experiment7()

