from sbox_aux import *
import seaborn as sns
import matplotlib.pylab as plt

def get_s_inputs(k, p):
    # 1 2 3 4 5 6 7 8 9 10 (formato de p e p*)

    # p 1 2 3 4 5 6 5 6 7  8  9 10 (entrada pra S-Box conjunta, já que 5 e 6 são compartilhados)
    # k 1 2 3 4 5 6 7 8 9 10 11 12
    # k 0 0 0 0 1 2 3 4 0  0  0 0
    mask1 = 0b1111110000
    mask2 = 0b0000111111

    first_two_key_bits = k >> 2
    last_two_key_bits = (k & 0b0011)

    s1_input = ((p & mask1) >> 4) ^ first_two_key_bits
    s2_input = (p & mask2) ^ (last_two_key_bits << 4)

    return s1_input, s2_input

def get_s_outputs(sbox1, sbox2, s1_input, s2_input):
    s1_output = get_sbox_result(sbox1, s1_input)
    s2_output = get_sbox_result(sbox2, s2_input)
    y = (s1_output << 4) | s2_output
    return y

def fill_ddt(sbox1, sbox2):
    ddt2 = [ [ [ 0 for i in range(2**8) ] for j in range(2**10) ] for k in range(2**4) ]

    for k in range(0, 2**4): # 4 bits de chave são compartilhados
        print("Preenchendo DDT para k =", k)
        for p in range(0, 2**10): # texto claro p
            for p_star in range(0, 2**10): # texto claro p*

                s1_input, s2_input = get_s_inputs(k, p)
                s1_star_input, s2_star_input = get_s_inputs(k, p_star)

                y = get_s_outputs(sbox1, sbox2, s1_input, s2_input)
                y_ = get_s_outputs(sbox1, sbox2, s1_star_input, s2_star_input)

                input_diff = p ^ p_star
                output_diff = y ^ y_

                ddt2[k][input_diff][output_diff]+=1

    return ddt2

def print_ddt_column(ddt, od):
    for k in range(0, 2**4):
        for id in range(0, 2**10):
            print("k", k, "id", id, "od", od, ddt[k][x][od])

def print_ddt_column_important_ids(ddt, od):
    print("Checking correctness...")
    for k in range(0, 2**4):
        for id in range(0, 2**6):
            if ddt[k][id << 2][od] != 0 and ddt[k][id << 2][od] != 1024:
                print("k", k, "id", id << 2, "od", od, ddt[k][id << 2][od])
                print("THIS TABLE IS WRONG")

def ddt_to_csv(sbox1, sbox2, joint_ddt, key):
    A = np.array(joint_ddt[key])
    df_cols = []
    for i in range(2**8):
        df_cols.append(str(i))

    my_df = pd.DataFrame(A, columns=df_cols)
    #my_df.index += 1
    my_df.to_csv("ddt2/des_joint_ddt_"+str(sbox1)+"_"+str(sbox2)+"_"+str(key)+".csv")

def heatmap(ddt, maxval):
    ax = sns.heatmap(ddt, linewidth=0.5, vmax=maxval, cmap="YlGnBu")
    plt.show()

def differential_uniformity(ddt):
    maximum = 0
    maxid = 0
    maxod = 0
    for id in range(2**10):
        for od in range(2**8):
            if id != 0 or od != 0:
                if ddt[id][od] > maximum:
                    maximum = ddt[id][od]
                    maxid = id
                    maxod = od
    return maximum, maxid, hex(maxod)

ddt = fill_ddt(int(sys.argv[1]), int(sys.argv[2]))
#print_ddt_column_important_ids(ddt, int(sys.argv[1]))
for k in range(2**4):
    #ddt_to_csv(8, 1, ddt, k)
    print_ddt_column_important_ids(ddt, 0)
    du = differential_uniformity(ddt[k])
    print("Differential uniformity for k =", k, "is", du)
    #heatmap(ddt[k], du[0])
