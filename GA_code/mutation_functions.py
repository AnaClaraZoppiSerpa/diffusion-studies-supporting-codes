import random

def mutation1(matrix, args):
    # Get the dimensions of the matrix
    rows = len(matrix)
    cols = len(matrix[0])

    # Generate random row and column indices
    random_row = random.randint(0, rows - 1)
    random_col = random.randint(0, cols - 1)

    new_matrix = [row[:] for row in matrix]

    # Change the value at the random position to 1
    new_matrix[random_row][random_col] = 1

    return new_matrix

def mutation2(matrix, args):
    # Get the dimensions of the matrix
    rows = len(matrix)
    cols = len(matrix[0])

    new_matrix = [row[:] for row in matrix]

    # Generate random positions and change them to 1
    num_elements = random.randint(1, rows*cols)
    for _ in range(num_elements):
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        new_matrix[random_row][random_col] = 1

    return new_matrix

def mutation3(matrix, args):
    # Get the dimensions of the matrix
    rows = len(matrix)
    cols = len(matrix[0])

    new_matrix = [row[:] for row in matrix]

    # Generate random row and column indices
    random_row = random.randint(0, rows - 1)
    random_col = random.randint(0, cols - 1)

    # Change the value at the random position to a random value inside the limits
    new_matrix[random_row][random_col] = random.randint(1, args.upper)

    return new_matrix

def mutation4(matrix, args):
    # Get the dimensions of the matrix
    rows = len(matrix)
    cols = len(matrix[0])

    new_matrix = [row[:] for row in matrix]

    # Generate random positions and change them to 1
    num_elements = random.randint(1, rows*cols)
    for _ in range(num_elements):
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        new_matrix[random_row][random_col] = random.randint(1, args.upper)

    return new_matrix
