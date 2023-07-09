import sys

diffusion_map = {}

def print_map(dmap):
    for key in dmap:
        print(key, "depends on ", dmap[key])

    for key in dmap:
        print(key, "depends on ", len(dmap[key]), "bits of the plaintext")

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
        output_node = str(output_bit) + "_" + str(round)

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
        output_node = str(output_bit) + "_" + str(round)
        add_edges(output_node, [input_node_left, input_node_right])

def apply_F(bit_start, bit_end, round):
    for current_slice in range(bit_start, bit_end, 4):
        full_diffusion_sbox(current_slice, current_slice+3, round)
        extension_function(current_slice, current_slice+3, bit_start, bit_end, round)

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

        l += 1
        r += 1

for r in range(1, 17):
    feistel_left_equals_previous_right(1, 32, 33, 64, r)
    apply_F(33, 64, r)
    feistel_bitwise_xor(33, 64, 1, 32, r)

print("Map generated with set arithmethic")
print_map(diffusion_map)
