import sys
import numpy as np
import pandas as pd
import csv

start = int(1) #sys.argv[1]
end = int(16) #sys.argv[2]

diffusion_map = {}

permutation = [0, 16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
matrix = [[0]*64 for i in range(64)]

key_diff_map = {}

def print_key_map():
    for state_bit in key_diff_map:
        print(state_bit, "->", key_diff_map[state_bit])

def print_key_map_amounts():
    for state_bit in key_diff_map:
        if state_bit[0] not in ["K", "C", "D", "b", "T"]:
            print(state_bit, "->", len(key_diff_map[state_bit]))

def get_round_mins_and_maxs():
    mins_and_maxs = {}
    for i in range(start, end+1):
        mins_and_maxs[str(i)] = {}
        mins_and_maxs[str(i)]["min"] = 100
        mins_and_maxs[str(i)]["max"] = -1

    for state_bit in key_diff_map:
        if state_bit[0] not in ["K", "C", "D", "b", "T"]:
            bit, round = state_bit.split("_")
            diff = len(key_diff_map[state_bit])

            mins_and_maxs[round]["min"] = min(mins_and_maxs[round]["min"], diff)
            mins_and_maxs[round]["max"] = max(mins_and_maxs[round]["max"], diff)

    f = open("des_intermediate_keys.csv", "a")
    writer = csv.writer(f)
    writer.writerow(["start", "end", "round", "min", "max"])
    for i in range(start, end+1):
        print(i, "min", mins_and_maxs[str(i)]["min"], "max", mins_and_maxs[str(i)]["max"])
        writer.writerow([start, end, i, mins_and_maxs[str(i)]["min"], mins_and_maxs[str(i)]["max"]])

    #print(mins_and_maxs)

def map_aux(dmap):
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
                else: # key part
                    dependent_state_bit = key
                    round_key_bit = plaintext_element
                    #print(dependent_state_bit, "depends on", round_key_bit)
                    add_key_edge(dependent_state_bit, round_key_bit)

    for key in dmap:
        if key[0] != "s":
            #print(key, "depends on", len(dmap[key]), "bits of the plaintext")
            pass

def add_key_edge(dependent_bit, key_bit):
    if dependent_bit in key_diff_map:
        add_node_to_key_set(dependent_bit, key_bit)
    else:
        key_diff_map[dependent_bit] = set()
        add_node_to_key_set(dependent_bit, key_bit)

def add_node_to_key_set(state_bit, key_bit):
    if key_bit in key_diff_map:
        key_diff_map[state_bit] |= key_diff_map[key_bit]
    else:
        key_diff_map[state_bit].add(key_bit)

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
        #print(input_node, "goes to", output_node)

def apply_F(bit_start, bit_end, round):
    slice_count = 1
    for current_slice in range(bit_start, bit_end, 4):
        #print("current slice = ", slice_count)
        full_diffusion_sbox(current_slice, current_slice+3, round)
        extension_function(current_slice, current_slice+3, bit_start, bit_end, round)

        round_key_bit_upper_bound = 6 * slice_count
        round_key_bit_lower_bound = round_key_bit_upper_bound - 5

        round_key_nodes = []
        for round_key_bit in range(round_key_bit_lower_bound, round_key_bit_upper_bound+1):
            round_key_node = "K_" + str(round_key_bit) + "_" + str(round)
            #print("round_key_node = ", round_key_node)
            round_key_nodes.append(round_key_node)

        for s_bit in range(current_slice, current_slice+3+1):
            #print("sbit", s_bit, "depends on", round_key_nodes)
            s_node = "s" + str(s_bit) + "_" + str(round)
            if (round == 1 and s_bit == 45):
                print("round key nodes used here are ", round_key_nodes)
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

def key_schedule():
    left_shift_by_1 = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 1]
    left_shift_by_2 = [0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 1, 2]
    # to-do!
    PC1 = [0, 57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    PC2 = [0, 14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

    v = [0]

    for i in range(1, 16+1):
        if i == 1 or i == 2 or i == 9 or i == 16:
            v.append(1)
        else:
            v.append(2)

    #print(v)

    for b in range(1, len(PC1)):
        T_node = "T_"+str(b)
        k_node = "k_"+str(PC1[b])
        #print(T_node, "->", k_node)
        add_key_edge(T_node, k_node)

    for b in range(1, 28+1):
        C0_node = "C_0_"+str(b)
        T_node = "T_"+str(b)
        #print(C0_node, "->", T_node)
        add_key_edge(C0_node, T_node)

    for b in range(29, 56+1):
        D0_node = "D_0_"+str(b-28)
        T_node = "T_"+str(b)
        #print(D0_node, "->", T_node)
        add_key_edge(D0_node, T_node)

    for i in range(1, 16+1):
        for b in range(1, 28+1):
            C1_node = "C_"+str(i)+"_"+str(b)
            shift_result = left_shift_by_1[b]

            if v[i] == 1:
                shift_result = left_shift_by_1[b]
            elif v[i] == 2:
                shift_result = left_shift_by_2[b]

            C0_node = "C_"+str(i-1)+"_"+str(shift_result)
            add_key_edge(C1_node, C0_node)

        for b in range(1, 28+1):
            D1_node = "D_"+str(i)+"_"+str(b)

            if v[i] == 1:
                shift_result = left_shift_by_1[b]
            elif v[i] == 2:
                shift_result = left_shift_by_2[b]

            D0_node = "D_"+str(i-1)+"_"+str(shift_result)
            add_key_edge(D1_node, D0_node)

        for b in range(1, 28+1):
            b_node = "b_"+str(i)+"_"+str(b)
            C1_node = "C_"+str(i)+"_"+str(b)
            add_key_edge(b_node, C1_node)

        for b in range(29, 56+1):
            b_node = "b_"+str(i)+"_"+str(b)
            D1_node = "D_"+str(i)+"_"+str(b-28)
            add_key_edge(b_node, D1_node)

        for b in range(1, 48+1):
            subkey_node = "K_"+str(b)+"_"+str(i)
            b_node = "b_"+str(i)+"_"+str(PC2[b])
            #print(subkey_node, "->", b_node)
            add_key_edge(subkey_node, b_node)

    #print_key_map()
    print_subkeys(int(sys.argv[1]), int(sys.argv[2]))

def print_subkeys(round, bit):
    print("K_"+str(bit)+"_"+str(round), "->", key_diff_map["K_"+str(bit)+"_"+str(round)])

def generate_adjacency_list():
    key_schedule()

    for r in range(1, 17):
        feistel_left_equals_previous_right(1, 32, 33, 64, r)
        apply_F(33, 64, r)
        feistel_bitwise_xor(33, 64, 1, 32, r)

    #print("Map generated with set arithmethic")
    map_aux(diffusion_map)
    #print_key_map()
    print_key_map_amounts()

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
    map_aux(diffusion_map)

#def get_results():
#    generate_one_iteration_matrix()
#    A = np.array(matrix)
#    A_ = np.linalg.matrix_power(A, int(sys.argv[1])).tolist()
#    print_matrix(A_)

#    df_cols = []
#    for i in range(64):
#        df_cols.append(str(i+1))

#    my_df = pd.DataFrame(A_, columns=df_cols)
#    my_df.index += 1
#    my_df.to_csv("des_difusao_iteracao_"+str(sys.argv[1])+".csv")

def test_different_rounds(starting_from, ending_at):
    key_schedule()

    for r in range(starting_from, ending_at+1):
        feistel_left_equals_previous_right(1, 32, 33, 64, r)
        apply_F(33, 64, r)
        feistel_bitwise_xor(33, 64, 1, 32, r)

    #print("Map generated with set arithmethic")
    map_aux(diffusion_map)
    print_key_map()
    print_key_map_amounts()
    get_round_mins_and_maxs()

if __name__ == '__main__':
    #generate_adjacency_list()
    #key_schedule()
    test_different_rounds(int(sys.argv[1]),int(sys.argv[2]))
