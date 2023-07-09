from aes_sbox_aux import *
import numpy as np
import pandas as pd
import sys
import seaborn as sns
import matplotlib.pylab as plt

if sys.argv[1] == 'inv':
    S = aes_inv_sbox
else:
    S = aes_sbox

csv_path = "../results/aes_ddt"+sys.argv[1]+".csv"

def get_ddt():
    ddt = [ [ 0 for i in range(2**8) ] for j in range(2**8) ]
    for x in range(2**8):
        for x_ in range(2**8):
            y = S[x]
            y_ = S[x_]

            idiff = x ^ x_
            odiff = y ^ y_

            ddt[idiff][odiff] += 1
    return ddt

def print_ddt(ddt):
    A = np.array(ddt)
    df_cols = []
    for i in range(2**8):
        df_cols.append(hex(i))

    my_df = pd.DataFrame(A, columns=df_cols)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    #my_df.to_csv(csv_path)

    print(my_df)

def heatmap(ddt):
    ax = sns.heatmap(ddt, linewidth=0.5, vmax=4, cmap="YlGnBu")
    plt.show()

def differential_uniformity(ddt):
    maximum = 0
    maxid = 0
    maxod = 0
    for id in range(2**8):
        for od in range(2**8):
            if id != 0 or od != 0:
                if ddt[id][od] > maximum:
                    maximum = ddt[id][od]
                    maxid = id
                    maxod = od
    return maximum, maxid, hex(maxod)

d = get_ddt()
print_ddt(d)
heatmap(d)
print("Differential uniformity = ", differential_uniformity(d))
