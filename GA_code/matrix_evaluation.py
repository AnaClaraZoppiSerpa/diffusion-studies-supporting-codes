import galois
import numpy as np
import itertools

GF2 = galois.GF(2)


def poly_xtime_cost(poly, ORDER):
    if poly == 0:
        return 0
    degree = ORDER
    degree_mask = 2 ** ORDER

    while (poly & degree_mask) == 0:
        degree_mask = degree_mask >> 1
        degree -= 1
    return degree


def poly_xor_cost(poly, ORDER):
    mask = 1
    set_bits = 0
    current_bit = 0
    while current_bit < ORDER:
        if (poly & mask) != 0:
            set_bits += 1
        mask = mask << 1
        current_bit += 1
    return set_bits - 1


def matrix_xtime_cost(mat, ORDER):
    total_cost = 0
    for row in range(len(mat)):
        row_cost = 0
        for col in range(len(mat[row])):
            row_cost += poly_xtime_cost(mat[row][col], ORDER)
        total_cost += row_cost
    return total_cost


def matrix_xor_cost(mat, ORDER):
    total_cost = 0
    for row in range(len(mat)):
        row_cost = len(mat) - 1
        for col in range(len(mat[row])):
            row_cost += poly_xor_cost(mat[row][col], ORDER)
        total_cost += row_cost
    return total_cost


# Converter um inteiro pra um polinômio do pacote Galois
def int_to_gf(int_poly):
    coeffs = []
    for x in bin(int_poly)[2:]:
        coeffs.append(int(x))

    return galois.Poly(coeffs, field=GF2)


# Converter uma matriz de inteiros pra uma matriz com elementos de um corpo finito
def int_to_gf_mat(int_mat, field):
    rows = len(int_mat)
    cols = len(int_mat[0])

    gf_mat = field.Zeros((rows, cols))

    for i in range(rows):
        for j in range(cols):
            gf_mat[i][j] = int_mat[i][j]

    return gf_mat


# Ver se uma matriz é MDS, sendo essa matriz uma matriz com elementos de corpos finitos
def is_mds(mat_in_field):
    if np.linalg.det(mat_in_field) == 0:
        return False

    dim = len(mat_in_field)

    dim_list = [i for i in range(dim)]

    z = 1
    while z < dim:
        possibilities = list(itertools.combinations(dim_list, z))

        for rows_to_be_removed in possibilities:
            for columns_to_be_removed in possibilities:
                submat = np.delete(mat_in_field, rows_to_be_removed, axis=0)
                submat = np.delete(submat, columns_to_be_removed, axis=1)
                if np.linalg.det(submat) == 0:
                    return False
        z += 1
    return True
