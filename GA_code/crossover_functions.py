import random


def midpoint_crossover1(parent1, parent2):
    # Assuming parent1 and parent2 have the same dimensions

    # Get the dimensions of the parents
    rows = len(parent1)
    cols = len(parent1[0])

    # Calculate the midpoint index
    midpoint = rows * cols // 2

    # Flatten the parents
    parent1_flat = [val for row in parent1 for val in row]
    parent2_flat = [val for row in parent2 for val in row]

    # Create child matrices
    child1 = parent1_flat[:midpoint] + parent2_flat[midpoint:]
    child2 = parent2_flat[:midpoint] + parent1_flat[midpoint:]

    # Reshape the children to match the dimensions of the parents
    child1 = [child1[i * cols:(i + 1) * cols] for i in range(rows)]
    child2 = [child2[i * cols:(i + 1) * cols] for i in range(rows)]

    return child1, child2


def midpoint_crossover2(parent1, parent2):
    # Assuming parent1 and parent2 have the same dimensions

    # Get the dimensions of the parents
    rows = len(parent1)
    cols = len(parent1[0])

    # Create an empty child matrix
    child1 = [[0] * cols for _ in range(rows)]
    child2 = [[0] * cols for _ in range(rows)]

    # Perform midpoint crossover
    midpoint = cols // 2  # Calculate the midpoint

    for i in range(rows):
        child1[i][:midpoint] = parent1[i][:midpoint]
        child1[i][midpoint:] = parent2[i][midpoint:]
        child2[i][:midpoint] = parent2[i][:midpoint]
        child2[i][midpoint:] = parent1[i][midpoint:]

    return child1, child2


def alternating_crossover(parent1, parent2):
    # Assuming parent1 and parent2 have the same dimensions

    # Get the dimensions of the parents
    rows = len(parent1)
    cols = len(parent1[0])

    # Create an empty child matrix
    child1 = [[0] * cols for _ in range(rows)]
    child2 = [[0] * cols for _ in range(rows)]

    # Perform alternating crossover
    for i in range(rows):
        for j in range(cols):
            if (i + j) % 2 == 0:
                child1[i][j] = parent1[i][j]
                child2[i][j] = parent2[i][j]
            else:
                child1[i][j] = parent2[i][j]
                child2[i][j] = parent1[i][j]

    return child1, child2


def random_points_crossover1(parent1, parent2):
    # Assuming parent1 and parent2 have the same dimensions

    # Get the dimensions of the parents
    rows = len(parent1)
    cols = len(parent1[0])

    # Calculate the midpoint index
    upper = rows * cols
    midpoint = random.randint(0, upper)

    # Flatten the parents
    parent1_flat = [val for row in parent1 for val in row]
    parent2_flat = [val for row in parent2 for val in row]

    # Create child matrices
    child1 = parent1_flat[:midpoint] + parent2_flat[midpoint:]
    child2 = parent2_flat[:midpoint] + parent1_flat[midpoint:]

    # Reshape the children to match the dimensions of the parents
    child1 = [child1[i * cols:(i + 1) * cols] for i in range(rows)]
    child2 = [child2[i * cols:(i + 1) * cols] for i in range(rows)]

    return child1, child2


def random_points_crossover2(parent1, parent2):
    # Assuming parent1 and parent2 have the same dimensions

    # Get the dimensions of the parents
    rows = len(parent1)
    cols = len(parent1[0])

    # Create an empty child matrix
    child1 = [[0] * cols for _ in range(rows)]
    child2 = [[0] * cols for _ in range(rows)]

    # Perform midpoint crossover
    upper = cols
    midpoint = random.randint(0, upper)  # Calculate the midpoint

    for i in range(rows):
        child1[i][:midpoint] = parent1[i][:midpoint]
        child1[i][midpoint:] = parent2[i][midpoint:]
        child2[i][:midpoint] = parent2[i][:midpoint]
        child2[i][midpoint:] = parent1[i][midpoint:]

    return child1, child2


def random_points_crossover3(parent1, parent2):
    # Assuming parent1 and parent2 have the same dimensions

    # Get the dimensions of the parents
    rows = len(parent1)
    cols = len(parent1[0])

    # Create an empty child matrix
    child1 = [[0] * cols for _ in range(rows)]
    child2 = [[0] * cols for _ in range(rows)]

    # Perform midpoint crossover
    upper = cols

    for i in range(rows):
        midpoint = random.randint(0, upper)  # Calculate the midpoint
        child1[i][:midpoint] = parent1[i][:midpoint]
        child1[i][midpoint:] = parent2[i][midpoint:]
        child2[i][:midpoint] = parent2[i][:midpoint]
        child2[i][midpoint:] = parent1[i][midpoint:]

    return child1, child2


crossover1 = midpoint_crossover1
crossover2 = midpoint_crossover2
crossover3 = alternating_crossover
crossover4 = random_points_crossover1
crossover5 = random_points_crossover2
crossover6 = random_points_crossover3
