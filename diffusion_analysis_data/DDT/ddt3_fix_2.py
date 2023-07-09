from sbox_aux import *

ddt3 = {}

def get_s_inputs(k, p):
    mask1 = 0b11111100000000
    mask2 = 0b00001111110000
    mask3 = 0b00000000111111

    get_k1_and_k2_on_lsb = k >> 6
    get_k7_and_k8_on_msb = (k & 0b00000011) << 4

    get_k3_and_k4_on_msb = (k & 0b00110000)
    get_k5_and_k6_on_lsb = (k & 0b00001100) >> 2
    get_k3_k5_k5_k6_on_their_places = get_k3_and_k4_on_msb | get_k5_and_k6_on_lsb

    s1_p = (p & mask1) >> 8
    s2_p = (p & mask2) >> 4
    s3_p = (p & mask3)

    return s1_p ^ get_k1_and_k2_on_lsb, s2_p ^ get_k3_k5_k5_k6_on_their_places, s3_p ^ get_k7_and_k8_on_msb

def get_s_outputs(sbox1, sbox2, sbox3, s1_input, s2_input, s3_input):
    s1_output = get_sbox_result(sbox1, s1_input)
    s2_output = get_sbox_result(sbox2, s2_input)
    s3_output = get_sbox_result(sbox3, s3_input)

    y = (s1_output << 8) | (s2_output << 4) | (s3_output)
    return y

def init_dict():
    for id in range(2**14):
        ddt3[id & 0b00111111111100] = 0

def calculate(k, sbox1, sbox2, sbox3):
    for p in range(2**14):
        for p_ in range(2**14):
            input_diff = p ^ p_
            if input_diff in ddt3:
                s1_input, s2_input, s3_input = get_s_inputs(k, p)
                s1_star_input, s2_star_input, s3_start_input = get_s_inputs(k, p_)

                y = get_s_outputs(sbox1, sbox2, sbox3, s1_input, s2_input, s3_input)
                y_ = get_s_outputs(sbox1, sbox2, sbox3, s1_star_input, s2_star_input, s3_start_input)

                output_diff = y ^ y_
                #print(input_diff, hex(input_diff), bin(input_diff))

                if output_diff == 0:
                    ddt3[input_diff] += 1

def print_ddt():
    for id in sorted(ddt3):
        if ddt3[id] != 0:
            print("id =", hex(id), "col =", ddt3[id])

print("Key:", sys.argv[1], "S-Boxes:", sys.argv[2], sys.argv[3], sys.argv[4])
init_dict()
#print("Conseguiu inicializar")
calculate(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
#print("Consegue calcular")
print_ddt()
