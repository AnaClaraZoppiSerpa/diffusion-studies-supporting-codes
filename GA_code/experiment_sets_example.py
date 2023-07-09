from ga import *


def experiment1():
    E = ExperimentSettings(4, 3, GF2_4)
    A = Arguments(E.integer_upper_limit, 6, 6, 6, 3, 10, 5, 8, 0.1)
    F = ChosenFunctions(random_initialization,
                        selection1,
                        pairing1,
                        crossover1,
                        mutation1,
                        replacement1)
    evolve(E, A, F, "experiment1()")


def experiment2():
    E = ExperimentSettings(4, 3, GF2_4)
    A = Arguments(E.integer_upper_limit, 6, 6, 6, 3, 10, 5, 8, 0.1)
    F = ChosenFunctions(random_initialization,
                        selection1,
                        pairing1,
                        crossover1,
                        mutation1,
                        replacement1)
    evolve(E, A, F, "experiment2()")


def experiment3():
    E = ExperimentSettings(4, 3, GF2_4)
    A = Arguments(E.integer_upper_limit, 6, 6, 6, 3, 10, 5, 8, 0.1)
    F = ChosenFunctions(random_initialization,
                        selection1,
                        pairing1,
                        crossover1,
                        mutation1,
                        replacement1)
    evolve(E, A, F, "experiment3()")


experiment1()
experiment2()
experiment3()
