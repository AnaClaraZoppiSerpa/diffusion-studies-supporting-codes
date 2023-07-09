from sbox_aux import *

"""
====== S1 ======= |======== S2 ======= |=========== S3 ======= |
p1 p2 p3 p4 p5 p6 | p5 p6 p7 p8 p9 p10 | p9 p10 p11 p12 p13 p14
0  0  0  0  k1 k2 | k3 k4 0  0  k5 k6  | k7 k8  0   0   0   0
"""

def get_s_inputs(k, p):
    mask1 = 0b11111100000000
    mask2 = 0b00001111110000
    mask3 = 0b00000000111111

    get_k1_and_k2_on_lsb = k >> 6
    get_k7_and_k8_on_msb = (k & 0b00000011) << 4
    #print(bin(get_k1_and_k2_on_lsb))
    #print(bin(get_k7_and_k8_on_msb))

    get_k3_and_k4_on_msb = (k & 0b00110000)
    get_k5_and_k6_on_lsb = (k & 0b00001100) >> 2
    get_k3_k5_k5_k6_on_their_places = get_k3_and_k4_on_msb | get_k5_and_k6_on_lsb
    #print(bin(get_k3_k5_k5_k6_on_their_places))

    #first_two_key_bits = k >> 2
    #last_two_key_bits = (k & 0b0011)
    s1_p = (p & mask1) >> 8
    s2_p = (p & mask2) >> 4
    s3_p = (p & mask3)
    #print(bin(p))
    #print(bin(s1_p))
    #print(bin(s2_p))
    #print(bin(s3_p))

    return s1_p ^ get_k1_and_k2_on_lsb, s2_p ^ get_k3_k5_k5_k6_on_their_places, s3_p ^ get_k7_and_k8_on_msb

def get_s_outputs(sbox1, sbox2, sbox3, s1_input, s2_input, s3_input):
    s1_output = get_sbox_result(sbox1, s1_input)
    s2_output = get_sbox_result(sbox2, s2_input)
    s3_output = get_sbox_result(sbox3, s3_input)

    y = (s1_output << 8) | (s2_output << 4) | (s3_output)
    #print(bin(s1_output))
    #print(bin(s2_output))
    #print(bin(s3_output))
    #print(bin(y))

    #y = (s1_output << 4) | s2_output
    return y

def get_s_inputs_zeroes(k, p):
    s1_p = (0b110000 & p) >> 2
    s2_p = (0b001100 & p)
    s3_p = (0b000011 & p) << 2

    get_k1_and_k2_on_lsb = k >> 6
    get_k7_and_k8_on_msb = (k & 0b00000011) << 4
    #print(bin(get_k1_and_k2_on_lsb))
    #print(bin(get_k7_and_k8_on_msb))

    get_k3_and_k4_on_msb = (k & 0b00110000)
    get_k5_and_k6_on_lsb = (k & 0b00001100) >> 2
    get_k3_k5_k5_k6_on_their_places = get_k3_and_k4_on_msb | get_k5_and_k6_on_lsb

    #print(bin(p))
    #print(bin(k))
    #print(bin(s1_p)[2:].zfill(6), "xor", bin(get_k1_and_k2_on_lsb)[2:].zfill(6))
    #print(bin(s2_p)[2:].zfill(6), "xor", bin(get_k3_k5_k5_k6_on_their_places)[2:].zfill(6))
    #print(bin(s3_p)[2:].zfill(6), "xor", bin(get_k7_and_k8_on_msb)[2:].zfill(6))

    return s1_p ^ get_k1_and_k2_on_lsb, s2_p ^ get_k3_k5_k5_k6_on_their_places, s3_p ^ get_k7_and_k8_on_msb

def fill_relevant_ddt(sbox1, sbox2, sbox3):
    """
    ====== S1 ======= |======== S2 ======= |=========== S3 ======= |
    p1 p2 p3 p4 p5 p6 | p5 p6 p7 p8 p9 p10 | p9 p10 p11 p12 p13 p14
    0  0  0  0  k1 k2 | k3 k4 0  0  k5 k6  | k7 k8  0   0   0   0

    Textos com o seguinte formato:
    0 0 p3 p4 0 0 | 0 0 p7 p8 0 0 | 0 0 p11 p12 0 0

    p3 p4 p7 p8 p11 p12
    """
    #ddt3 = [ [ 0 for i in range(2**6) ] for k in range(2**8) ]
    ddt3 = [ [ [ 0 for i in range(4096) ] for j in range(2**6) ] for k in range(2**8) ]
    max_od = 0
    for k in range(0, 2**8): # 8 bits de chave sendo compartilhados
        #print("Preenchendo pra k =", k)
        for p in range(0, 2**6):
            for p_star in range(0, 2**6):
                #print(k, p, p_star)
                s1_input, s2_input, s3_input = get_s_inputs_zeroes(k, p)
                s1_star_input, s2_star_input, s3_start_input = get_s_inputs_zeroes(k, p_star)

                y = get_s_outputs(sbox1, sbox2, sbox3, s1_input, s2_input, s3_input)
                y_ = get_s_outputs(sbox1, sbox2, sbox3, s1_star_input, s2_star_input, s3_start_input)

                input_diff = p ^ p_star
                output_diff = y ^ y_

                ddt3[k][input_diff][output_diff] += 1

    #print("ok")
    return ddt3

def print_relevant_ddt(ddt_dict, od):
    for k in range(2**8):
        print("Key:", k)
        for id in range(2**6):
            if ddt_dict[k][id][od] != 0:
                print("Input Difference:", id, "Output Difference:", od, "Count:", ddt_dict[k][id][od])

#get_s_inputs(0b11111111, 0b10101100110011)
#get_s_outputs(1, 2, 3, 1, 2, 3)

def ddt_to_csv(sbox1, sbox2, sbox3, joint_ddt, key):
    A = np.array(joint_ddt[key])
    df_cols = []
    for i in range(4096):
        df_cols.append(str(i))

    my_df = pd.DataFrame(A, columns=df_cols)
    #my_df.index += 1
    my_df.to_csv("ddt3/des_joint_ddt_"+str(sbox1)+"_"+str(sbox2)+"_"+str(sbox3)+"_"+str(key)+".csv")


ddt = fill_relevant_ddt(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
print_relevant_ddt(ddt, int(sys.argv[4]))
#ddt_to_csv(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), ddt, 0)
#get_s_inputs_zeroes(0b11111111, 0b101101)
#print_ddt_column(ddt, 0)
#print_ddt_column_important_ids(ddt, int(sys.argv[1]))
#for k in range(2**4):
    #ddt_to_csv(8, 1, ddt, k)
#    print_ddt_column_important_ids(ddt, 0)
