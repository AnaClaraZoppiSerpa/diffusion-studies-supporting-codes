import sys
import numpy as np
import pandas as pd

diffusion_map = {}

permutation = [0, 16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
matrix = [[0]*64 for i in range(64)]

def print_map(dmap):
    for key in dmap:
        if key[0] != "s":
            #print(key, "depends on", dmap[key])
            for plaintext_element in dmap[key]:
                if plaintext_element[0] != "K":
                    iteration_one_bit, round = key.split("_")
                    plaintext_bit, round_zero = plaintext_element.split("_")
                    #print("Iteration 1 bit", iteration_one_bit, "depends on plaintext bit", plaintext_bit)
                    #print("Updating indexes", int(plaintext_bit)-1, "and", int(iteration_one_bit)-1)
                    matrix[int(plaintext_bit)-1][int(iteration_one_bit)-1] = 1
                    #print(matrix)
                else:
                    print(key, "depends on", plaintext_element)

    for key in dmap:
        if key[0] != "s":
            #print(key, "depends on", len(dmap[key]), "bits of the plaintext")
            pass

def add_nodes_to_set(node, nodes):
    for n in nodes:
        if n in diffusion_map:
            diffusion_map[node] |= diffusion_map[n]
        else:
            diffusion_map[node].add(n)

def add_edges(node, dependency_nodes):
    if node in diffusion_map:
        add_nodes_to_set(node, dependency_nodes)
    else:
        diffusion_map[node] = set()
        add_nodes_to_set(node, dependency_nodes)

def full_diffusion_sbox(bit_start, bit_end, round):
    input_nodes = []

    for input_bit in range(bit_start, bit_end+1):
        input_nodes.append(str(input_bit) + "_" + str(round-1))

    for output_bit in range(bit_start, bit_end+1):
        output_node = "s" + str(output_bit) + "_" + str(round)

        add_edges(output_node, input_nodes)

def extension_function(slice_start, slice_end, bits_start, bits_end, round):
    input_nodes = []
    left_expansion = slice_start - 1
    right_expansion = slice_end + 1

    if left_expansion < bits_start:
        left_expansion = bits_end

    if right_expansion > bits_end:
        right_expansion = bits_start

    input_node_left = str(left_expansion) + "_" + str(round-1)
    input_node_right = str(right_expansion) + "_" + str(round-1)

    for output_bit in range(slice_start, slice_end+1):
        output_node = "s" + str(output_bit) + "_" + str(round)
        add_edges(output_node, [input_node_left, input_node_right])

def permutation_P(bit_start, bit_end, round):
    for current_bit in range(bit_start, bit_end+1):
        permuted_bit = permutation[current_bit - 32] + 32

        input_node = "s" + str(permuted_bit) + "_" + str(round)

        output_node = str(current_bit) + "_" + str(round)
        add_edges(output_node, [input_node])
        #print(output_node, "is taken from", input_node)
        print(input_node, "goes to", output_node)

def apply_F(bit_start, bit_end, round):
    slice_count = 1
    for current_slice in range(bit_start, bit_end, 4):
        print("current slice = ", slice_count)
        full_diffusion_sbox(current_slice, current_slice+3, round)
        extension_function(current_slice, current_slice+3, bit_start, bit_end, round)

        round_key_bit_upper_bound = 6 * slice_count
        round_key_bit_lower_bound = round_key_bit_upper_bound - 5

        round_key_nodes = []
        for round_key_bit in range(round_key_bit_lower_bound, round_key_bit_upper_bound+1):
            round_key_node = "K_" + str(round_key_bit) + "_" + str(round)
            print("round_key_node = ", round_key_node)
            round_key_nodes.append(round_key_node)

        for s_bit in range(current_slice, current_slice+3+1):
            print("sbit", s_bit, "depends on", round_key_nodes)
            s_node = "s" + str(s_bit) + "_" + str(round)
            add_edges(s_node, round_key_nodes)

        slice_count += 1

    permutation_P(bit_start, bit_end, round)

def feistel_left_equals_previous_right(left_start, left_end, right_start, right_end, round):
    l = left_start
    r = right_start

    while l <= left_end and r <= right_end:
        r_node = str(r) + "_" + str(round-1)
        l_node = str(l) + "_" + str(round)

        add_edges(l_node, [r_node])

        l += 1
        r += 1

def feistel_bitwise_xor(right_start, right_end, left_start, left_end, round):
    r = right_start
    l = left_start

    while l <= left_end and r <= right_end:
        r_node = str(r) + "_" + str(round)
        l_node = str(l) + "_" + str(round-1)

        add_edges(r_node, [l_node])
        #print("XOR edge created:", r_node, "->", diffusion_map[l_node])

        l += 1
        r += 1

def generate_adjacency_list():
    for r in range(1, 17):
        feistel_left_equals_previous_right(1, 32, 33, 64, r)
        apply_F(33, 64, r)
        feistel_bitwise_xor(33, 64, 1, 32, r)

    print("Map generated with set arithmethic")
    print_map(diffusion_map)

def print_matrix(mat):
    header = "P\S "
    for i in range(64):
        if i+1 < 10:
            header += "0"
        header += str(i+1) + " "

    print(header)

    for plaintext_bit in range(64):
        row = "  "
        for e in mat[plaintext_bit]:
            row += str(e) + "  "

        pl = ""
        if plaintext_bit+1 < 10:
            pl = "0"

        pl += str(plaintext_bit+1)

        print(pl+row)

def generate_one_iteration_matrix():
    feistel_left_equals_previous_right(1, 32, 33, 64, 1)
    apply_F(33, 64, 1)
    feistel_bitwise_xor(33, 64, 1, 32, 1)
    print_map(diffusion_map)

def get_results():
    generate_one_iteration_matrix()
    A = np.array(matrix)
    A_ = np.linalg.matrix_power(A, int(sys.argv[1])).tolist()
    print_matrix(A_)

    df_cols = []
    for i in range(64):
        df_cols.append(str(i+1))

    my_df = pd.DataFrame(A_, columns=df_cols)
    my_df.index += 1
    my_df.to_csv("des_difusao_iteracao_"+str(sys.argv[1])+".csv")

if __name__ == '__main__':
    get_results()
