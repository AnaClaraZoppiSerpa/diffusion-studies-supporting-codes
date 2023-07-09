import galois
import math
import pprint
import sys
import datetime

from matrix_evaluation import *
from initial_population_functions import *
from selection_functions import *
from pairing_functions import *
from reproduction_functions import *
from crossover_functions import *
from mutation_functions import *
from replacement_functions import *
from lookup import *
from tee import *
from fitness_functions import *

BASELINES = {
    8: 296,
    4: 40,
    3: 15,
    2: 8,
    5: 120,
    6: 234,
    7: 384,
    16: 4544,
    32: 20032,
}

ONLY_XTIME_BASELINES = {2: 2, 3: 3, 4: 8, 5: 30, 6: 59, 7: 96, 8: 72, 16: 1248, 32: 5440}

GF2_4 = galois.GF(2 ** 4)
GF2_8 = galois.GF(2 ** 8)

FITNESS_FUNCTION = fitness_1

def get_existing_per_dim():
    existing_per_dimension = {}
    for matrix_id in LOOKUP_DICT:
        matrix = LOOKUP_DICT[matrix_id]
        dimension = len(matrix)
        if dimension in existing_per_dimension:
            existing_per_dimension[dimension].append(matrix)
        else:
            existing_per_dimension[dimension] = []
            existing_per_dimension[dimension].append(matrix)

    return existing_per_dimension

def applicable_in_field(m, upper_bound):
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] > upper_bound:
                return False
    return True
def filter_solutions_per_field_applicability(solutions, upper_bound):
    filtered = []
    for s in solutions:
        if applicable_in_field(s, upper_bound):
            filtered.append(s)
    return filtered


class Arguments:
    def __init__(self, upper, replacement_num_elites, replacement_num_survivors, replacement_tournament_size,
                 pairing_tournament_size, initial_population_size, max_iterations, selection_num_parents,
                 mutation_prob):
        self.upper = upper
        self.num_elites = replacement_num_elites
        self.num_survivors = replacement_num_survivors
        self.tournament_size = replacement_tournament_size
        self.pairing_tournament_size = pairing_tournament_size
        self.initial_population_size = initial_population_size
        self.max_iterations = max_iterations
        self.selection_num_parents = selection_num_parents
        self.mutation_prob = mutation_prob


class ExperimentSettings:
    def __init__(self, order, dimension, field):
        self.order = order
        self.integer_upper_limit = 2 ** self.order - 1
        self.dimension = dimension
        self.field = field


class ChosenFunctions:
    def __init__(self, initialization_f, selection_f, pairing_f, crossover_f, mutation_f, replacement_f, fitness_f):
        self.initialization_f = initialization_f
        self.selection_f = selection_f
        self.pairing_f = pairing_f
        self.crossover_f = crossover_f
        self.mutation_f = mutation_f
        self.replacement_f = replacement_f
        self.fitness_f = fitness_f

class ExperimentReport:
    def __init__(self, settings, arguments, functions):
        self.population_tracker = []
        self.offspring_tracker = []
        self.settings = settings
        self.arguments = arguments
        self.functions = functions
        self.mds_worse = {}
        self.mds_same = {}
        self.mds_better = {}
        self.u_mds_worse = []
        self.u_mds_same = []
        self.u_mds_better = []
    def extract_unique_for_list(self, mds_list, unique_list):
        for iteration in mds_list:
            for candidate in mds_list[iteration]:
                if not already_in_list(unique_list, candidate):
                    unique_list.append(candidate)
    def extract_unique(self):
        self.extract_unique_for_list(self.mds_worse, self.u_mds_worse)
        self.extract_unique_for_list(self.mds_same, self.u_mds_same)
        self.extract_unique_for_list(self.mds_better, self.u_mds_better)

def already_in_list(list, new_element):
    for list_element in list:
        if matrix_equals(list_element["matrix"], new_element["matrix"]):
            return True
    return False

class Candidate:
    def __init__(self, matrix, mds, invertible, xor, xtime, inverse, dim):
        self.matrix = matrix
        self.mds = mds
        self.invertible = invertible
        self.xor = xor
        self.xtime = xtime
        self.inverse = inverse
        self.dim = dim

        if len(sys.argv) > 2 and "xt-only" in sys.argv:
            self.cost = self.xtime
            self.baseline_diff = self.cost - ONLY_XTIME_BASELINES[dim]
        else:
            self.cost = 3 * self.xtime + 1 * self.xor
            self.baseline_diff = self.cost - BASELINES[dim]

        if self.baseline_diff > 0:
            self.ranking = "WORSE"
        if self.baseline_diff == 0:
            self.ranking = "SAME"
        if self.baseline_diff < 0:
            self.ranking = "BETTER"

        self.already_exists = False
        self.dataset_id = ""

        lookup = exists_in_dataset(LOOKUP_DICT, self.matrix)
        if lookup[0]:
            self.already_exists = True
            self.dataset_id = lookup[1]

    def fitness(self):
        return FITNESS_FUNCTION(self)


def get_candidate_data(mat, field, poly_order):
    dim = len(mat)
    is_invertible = True
    alg_mat = int_to_gf_mat(mat, field)
    inv = None

    is_mds_mat = is_mds(alg_mat)
    mat_xor = matrix_xor_cost(alg_mat, poly_order)
    mat_xtime = matrix_xtime_cost(alg_mat, poly_order)

    try:
        inv = np.linalg.inv(alg_mat)
    except:
        is_invertible = False

    return Candidate(mat, is_mds_mat, is_invertible, mat_xor, mat_xtime, inv, dim)


def to_candidates(list_of_matrices, E):
    candidates = []
    for matrix in list_of_matrices:
        c = get_candidate_data(matrix, E.field, E.order)
        candidates.append(c)
    return candidates
def to_dict_array(candidates):
    array = []
    for c in candidates:
        array.append(c.__dict__)
    return array

def add_to_dict(dict, i, c):
    if i not in dict:
        dict[i] = []
    if not already_in_list(dict[i], c):
        dict[i].append(c)

def add_to_correct_dict(R, i, c):
    if c["ranking"] == "WORSE":
        add_to_dict(R.mds_worse, i, c)
    elif c["ranking"] == "SAME":
        add_to_dict(R.mds_same, i, c)
    elif c["ranking"] == "BETTER":
        add_to_dict(R.mds_better, i, c)
def store_relevant_info(R, i):
    population = R.population_tracker[i]
    offspring = R.offspring_tracker[i]

    for c in population:
        if c["mds"]:
            print("(population) MDS candidate present at iteration", i, "ranking=", c["ranking"])
            add_to_correct_dict(R, i, c)
            print(c["matrix"])
        if c["ranking"] == "SAME" or c["ranking"] == "BETTER":
            print("DISCOVERY!!!")

    for c in offspring:
        if c["mds"]:
            print("(offspring) MDS candidate present at iteration", i, "ranking=", c["ranking"])
            add_to_correct_dict(R, i, c)
            print(c["matrix"])
        if c["ranking"] == "SAME" or c["ranking"] == "BETTER":
            print("DISCOVERY!!!")

def print_summary(R):
    print("MDS better")

    for m in R.u_mds_better:
        print("xor", m["xor"], "xtime", m["xtime"], "baseline diff", m["baseline_diff"])
        print(m["matrix"])

    print("MDS same")

    for m in R.u_mds_same:
        print("xor", m["xor"], "xtime", m["xtime"], "baseline diff", m["baseline_diff"])
        print(m["matrix"])

    print("MDS worse")

    for m in R.u_mds_worse:
        print("xor", m["xor"], "xtime", m["xtime"], "baseline diff", m["baseline_diff"])
        print(m["matrix"])

def evolution_stats(candidates):
    # Check if the list is empty
    if not candidates:
        print("Empty population.")
        return

    # Initialize variables
    min_fitness = float('inf')
    max_fitness = float('-inf')
    fitness_sum = 0
    num_elements = 0
    num_mds = 0

    # Iterate through the candidates
    for candidate in candidates:
        candidate_fitness = candidate.fitness()
        min_fitness = min(min_fitness, candidate_fitness)
        max_fitness = max(max_fitness, candidate_fitness)
        fitness_sum += candidate_fitness
        num_elements += 1
        if candidate.mds:
            num_mds += 1

    # Calculate the average fitness
    average_fitness = fitness_sum / num_elements

    # Print the results
    print(f"n={num_elements} mds={num_mds} min={min_fitness} max={max_fitness} sum={fitness_sum} avg={average_fitness}")


def evolve(E, A, F, fun):
    A.existing_solutions = filter_solutions_per_field_applicability(get_existing_per_dim()[E.dimension], E.integer_upper_limit)

    global FITNESS_FUNCTION

    FITNESS_FUNCTION = F.fitness_f

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    command_line = ""
    if len(sys.argv) > 1:
        command_line = sys.argv[1]

    log_file_path = "EXP/log-" + command_line + "-" + fun + "-" + timestamp
    log_file = open(log_file_path, 'w')
    full_data_path = "EXP/full-" + command_line + "-" + fun + "-" + timestamp
    full_data_file = open(full_data_path, 'w')
    compact_path = "EXP/relevant-" + command_line + "-" + fun + "-" + timestamp
    compact_file = open(compact_path, "w")

    R = ExperimentReport(E.__dict__, A.__dict__, F.__dict__)

    sys.stdout = Tee(sys.__stdout__, log_file, compact_file)
    print("EXPERIMENT IDENTIFICATION:", command_line, fun, timestamp)

    sys.stdout = Tee(log_file)
    print("EXPERIMENT PARAMETERS")
    print(E.__dict__)
    print(A.__dict__)
    print(F.__dict__)

    population = to_candidates(
        F.initialization_f(A.initial_population_size, E.integer_upper_limit, E.dimension, E.dimension, A), E)

    iteration_count = 0

    while iteration_count < A.max_iterations:
        sys.stdout = Tee(log_file, sys.__stdout__, compact_file)
        print(f"ITERATION {iteration_count+1} / {A.max_iterations}")

        R.population_tracker.append(to_dict_array(population))
        evolution_stats(population)

        selected_parents = F.selection_f(population, A.selection_num_parents)
        parent_pairs = F.pairing_f(selected_parents, A)
        offspring = to_candidates(reproduction(parent_pairs, A.mutation_prob, F.crossover_f, F.mutation_f, A), E)

        R.offspring_tracker.append(to_dict_array(offspring))

        sys.stdout = Tee(log_file)
        store_relevant_info(R, iteration_count)

        population = F.replacement_f(population, offspring, A)

        iteration_count += 1

    R.extract_unique()

    print("SUMMARY")
    print_summary(R)

    sys.stdout = Tee(full_data_file)

    print("EXPERIMENT FULL DATA", command_line, fun, timestamp)
    pprint.pprint(R.__dict__)

    sys.stdout = Tee(sys.__stdout__, log_file, compact_file)
    total_matrices_generated_estimate = A.selection_num_parents * 2 * A.max_iterations + A.initial_population_size
    ratio = (len(R.u_mds_better) + len(R.u_mds_same) + len(R.u_mds_worse)) / total_matrices_generated_estimate
    print(f"MDS better {len(R.u_mds_better)}, MDS same {len(R.u_mds_same)}, MDS worse {len(R.u_mds_worse)}, total {total_matrices_generated_estimate}, ratio = {ratio}")

    sys.stdout = sys.__stdout__
    log_file.close()
    full_data_file.close()
    compact_file.close()
