import sys

diffusion_map = {}
diffusion_map2 = {}
real_diffusion_map = {}

def print_observed_key(dmap, key):
    if key in dmap:
        print(key, "depends on ", len(dmap[key]), "bits of the plaintext")
        print(key, "depends on ", dmap[key])

def print_map(dmap):
    for key in dmap:
        print(key, "depends on ", dmap[key])

    for key in dmap:
        if key[0] != "s":
            print(key, "depends on ", len(dmap[key]), "bits of the plaintext")

def recur_in_graph(root, map_key):
    if root in diffusion_map2:
        for children in diffusion_map2[root]:
            recur_in_graph(children, map_key)
    else:
        if map_key in real_diffusion_map:
            real_diffusion_map[map_key].add(root)
        else:
            real_diffusion_map[map_key] = set()
            real_diffusion_map[map_key].add(root)

def add_nodes_to_set(node, nodes):
    for n in nodes:
        if n in diffusion_map:
            diffusion_map[node] |= diffusion_map[n]
        else:
            diffusion_map[node].add(n)

    if node not in diffusion_map2:
        diffusion_map2[node] = set()
    for n in nodes:
        diffusion_map2[node].add(n)

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
    # Bits 1, 2, 3, 4 -> 32, bits, 5
    # Bits 5, 6, 7, 8 -> 4, bits, 9
    # Bits 9, 10, 11, 12 -> 8, bits, 13
    # Bits 29, 30, 31, 32 -> 28, bits, 1

    # Em geral, coloca slice_start - 1 e slice_end + 1
    # No entanto, se slice_start - 1 < bits_start, coloca bits_end
    # E, se slice_end + 1 > bits_end, coloca bits_start

    # Isso deve entrar como input_nodes
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
    permutation = [0, 16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

    for current_bit in range(bit_start, bit_end+1):
        permuted_bit = permutation[current_bit - 32] + 32

        input_node = "s" + str(permuted_bit) + "_" + str(round)

        output_node = str(current_bit) + "_" + str(round)
        add_edges(output_node, [input_node])
        #print(output_node, "is taken from", input_node)

def apply_F(bit_start, bit_end, round):
    for current_slice in range(bit_start, bit_end, 4):
        full_diffusion_sbox(current_slice, current_slice+3, round)
        extension_function(current_slice, current_slice+3, bit_start, bit_end, round)

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

#apply_F(1, 32, 1)
#print_map(diffusion_map)

for r in range(1, 17):
#    #print(r)
    feistel_left_equals_previous_right(1, 32, 33, 64, r)
    apply_F(33, 64, r)
    #print("Diffusion map after F for round", r)
    #print_observed_key(diffusion_map, "33_2")
    #print_observed_key(diffusion_map, "34_2")
    feistel_bitwise_xor(33, 64, 1, 32, r)
    #print("Diffusion map after XOR for round", r)
    #print_observed_key(diffusion_map, "33_2")
    #print_observed_key(diffusion_map, "34_2")

print("Map generated with set arithmethic")
print_map(diffusion_map)
#print(diffusion_map[sys.argv[1]])
#print("Result with recursion")
#recur_in_graph(sys.argv[1], sys.argv[1])
#print(real_diffusion_map[sys.argv[1]])
