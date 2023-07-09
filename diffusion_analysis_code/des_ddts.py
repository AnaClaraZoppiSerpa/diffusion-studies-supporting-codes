import sys
import numpy as np
import pandas as pd

ddt = [ [ 0 for i in range(16) ] for j in range(64) ]

S = [
        #S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],

        #S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],

        #S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],

        #S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],

        #S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],

        #S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],

        #S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],

        #S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]
    ]

def get_sbox(i):
    return S[i-1]

def get_sbox_result(which_sbox, input_int):
    row = get_sbox_row(input_int)
    col = get_sbox_col(input_int)
    return S[which_sbox-1][row][col]

def get_sbox_row(input_int):
    binary = bin(input_int)[2:].zfill(6)
    first = binary[0]
    last = binary[-1]
    return int(first+last, 2)

def get_sbox_col(input_int):
    binary = bin(input_int)[2:].zfill(6)
    four_middle_bits = binary[1:-1]
    return int(four_middle_bits, 2)

def print_ddt():
    header = "     "
    for j in range(0, 16):
        header += str(hex(j).upper()[2:]) + "  "
        header += ""

    print(header)
    print("----------------------------------------------------")

    for i in range(0, 64):
        row = str(hex(i).upper()[2:]) + " "
        if len(str(hex(i)[2:])) < 2:
            row += " "
        row += "| "
        for j in range(0, 16):
            row += str(ddt[i][j]) + " "
            if ddt[i][j] < 10:
                row += " "
        print(row)

def get_ddt(which_sbox):
    for x in range(0, 64): # 64 chamadas
        for x_star in range(0, 64): # 64 chamadas -> 64*64
            y = get_sbox_result(which_sbox, x) # dimensão 6x4
            y_star = get_sbox_result(which_sbox, x_star) # dimensão 6x4

            # 64*64*2 chamadas a caixa S

            # 2^6 = 64 ->
            # de 0 até 2^N-1 (N: tamanho de entrada da caixa S)

            # (2^N) * (2^N) * 2 .... (2^N)^2 * 2
            # NxM -> mas depende só da entrada (N), não depende do M.

            input_diff = x ^ x_star # O(1)
            output_diff = y ^ y_star # O(1)

            dft[input_diff][output_diff] += 1

#get_ddt(int(sys.argv[1]))
#print_ddt()

def test_mask():
    for x in range(0, 2**10):
        mask1 = 0b1111110000
        mask2 = 0b0000111111
        print("x = ", bin(x), "mask1 =", bin(x & mask1), "mask2 =", bin(x & mask2))

def test_mask2():
    for x1 in range(0, 2**4):
        for x2 in range(0, 2**4):
            x = (x1 << 4) | x2
            print("x1 = ", bin(x1), "x2 =", bin(x2), "x =", bin(x))

joint_ddt = [ [ 0 for i in range(2**8) ] for j in range(2**10) ]
def get_joint_ddt(sbox1, sbox2):
    for x in range(0, 2**10):
        for x_ in range(0, 2**10):
            mask1 = 0b1111110000
            mask2 = 0b0000111111
            xs1input = (x & mask1) >> 4
            xs2input = x & mask2
            x_s1input = (x_ & mask1) >> 6
            x_s2input = x_ & mask2

            #print("x = ", bin(x), "s1 =", bin(xs1input), "s2 =", bin(xs2input))
            #print("x = ", x, "s1 =", xs1input, "s2 =",xs2input)
            #print("X = ", bin(x), "S1 =", bin(xs1input), "S2 =", bin(xs2input))

            ys1output = get_sbox_result(sbox1, xs1input)
            ys2output = get_sbox_result(sbox2, xs2input)
            y_s1output = get_sbox_result(sbox1, x_s1input)
            y_s2output = get_sbox_result(sbox2, x_s2input)

            y = (ys1output << 4) | ys2output
            y_ = (y_s1output << 4) | y_s2output

            input_diff = x ^ x_
            output_diff = y ^ y_

            #print(input_diff)

            joint_ddt[input_diff][output_diff] += 1

def print_joint_ddt():
    A = np.array(joint_ddt)
    df_cols = []
    for i in range(2**8):
        df_cols.append(hex(i))

    my_df = pd.DataFrame(A, columns=df_cols)
    my_df.index += 1
    my_df.to_csv("des_joint_ddt_1_2.csv")
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.max_rows', None)

    #writePath = 'des_joind_ddt_1_2.txt'
    #with open(writePath, 'a') as f:
    #    dfAsString = my_df.to_string()
    #    f.write(dfAsString)

    for i in range(2**10):
        print(hex(i))

get_joint_ddt(1, 2)
print_joint_ddt()

"""
00 00 00

00 01 00 -> 4 -> 4

00 10 00 -> 8 -> 8

00 11 00 -> 12 -> c

Essas 4 linhas ativam só 1 caixa S. As outras ativam mais de uma.
Queremos ativar uma caixa S por vez pra maximizar a probabilidade.
Apenas em 2 tabelas o valor máximo 16 aparece nessas 4 linhas de interesse.

O projeto do DES tenta evitar isso, ativando sempre mais de uma caixa S por vez.



     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F
----------------------------------------------------
0  | 64 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  ****
1  | 0  0  0  6  0  2  4  4  0  10 12 4  10 6  2  4
2  | 0  0  0  8  0  4  4  4  0  6  8  6  12 6  4  2
3  | 14 4  2  2  10 6  4  2  6  4  4  0  2  2  2  0
4  | 0  0  0  6  0  10 10 6  0  4  6  4  2  8  6  2  ****
5  | 4  8  6  2  2  4  4  2  0  4  4  0  12 2  4  6
6  | 0  4  2  4  8  2  6  2  8  4  4  2  4  2  0  12
7  | 2  4  10 4  0  4  8  4  2  4  8  2  2  2  4  4
8  | 0  0  0  12 0  8  8  4  0  6  2  8  8  2  2  4  ****
9  | 10 2  4  0  2  4  6  0  2  2  8  0  10 0  2  12
A  | 0  8  6  2  2  8  6  0  6  4  6  0  4  0  2  10
B  | 2  4  0  10 2  2  4  0  2  6  2  6  6  4  2  12
C  | 0  0  0  8  0  6  6  0  0  6  6  4  6  6  14 2  ****
D  | 6  6  4  8  4  8  2  6  0  6  4  6  0  2  0  2
E  | 0  4  8  8  6  6  4  0  6  6  4  0  0  4  0  8
F  | 2  0  2  4  4  6  4  2  4  8  2  2  2  6  8  8
10 | 0  0  0  0  0  0  2  14 0  6  6  12 4  6  8  6
11 | 6  8  2  4  6  4  8  6  4  0  6  6  0  4  0  0
12 | 0  8  4  2  6  6  4  6  6  4  2  6  6  0  4  0
13 | 2  4  4  6  2  0  4  6  2  0  6  8  4  6  4  6
14 | 0  8  8  0  10 0  4  2  8  2  2  4  4  8  4  0
15 | 0  4  6  4  2  2  4  10 6  2  0  10 0  4  6  4
16 | 0  8  10 8  0  2  2  6  10 2  0  2  0  6  2  6
17 | 4  4  6  0  10 6  0  2  4  4  4  6  6  6  2  0
18 | 0  6  6  0  8  4  2  2  2  4  6  8  6  6  2  2
19 | 2  6  2  4  0  8  4  6  10 4  0  4  2  8  4  0
1A | 0  6  4  0  4  6  6  6  6  2  2  0  4  4  6  8
1B | 4  4  2  4  10 6  6  4  6  2  2  4  2  2  4  2
1C | 0  10 10 6  6  0  0  12 6  4  0  0  2  4  4  0
1D | 4  2  4  0  8  0  0  2  10 0  2  6  6  6  14 0
1E | 0  2  6  0  14 2  0  0  6  4  10 8  2  2  6  2
1F | 2  4  10 6  2  2  2  8  6  8  0  0  0  4  6  4
20 | 0  0  0  10 0  12 8  2  0  6  4  4  4  2  0  12
21 | 0  4  2  4  4  8  10 0  4  4  10 0  4  0  2  8
22 | 10 4  6  2  2  8  2  2  2  2  6  0  4  0  4  10
23 | 0  4  4  8  0  2  6  0  6  6  2  10 2  4  0  10
24 | 12 0  0  2  2  2  2  0  14 14 2  0  2  6  2  4
25 | 6  4  4  12 4  4  4  10 2  2  2  0  4  2  2  2
26 | 0  0  4  10 10 10 2  4  0  4  6  4  4  4  2  0
27 | 10 4  2  0  2  4  2  0  4  8  0  4  8  8  4  4
28 | 12 2  2  8  2  6  12 0  0  2  6  0  4  0  6  2
29 | 4  2  2  10 0  2  4  0  0  14 10 2  4  6  0  4
2A | 4  2  4  6  0  2  8  2  2  14 2  6  2  6  2  2
2B | 12 2  2  2  4  6  6  2  0  2  6  2  6  0  8  4
2C | 4  2  2  4  0  2  10 4  2  2  4  8  8  4  2  6
2D | 6  2  6  2  8  4  4  4  2  4  6  0  8  2  0  6
2E | 6  6  2  2  0  2  4  6  4  0  6  2  12 2  6  4
2F | 2  2  2  2  2  6  8  8  2  4  4  6  8  2  4  2
30 | 0  4  6  0  12 6  2  2  8  2  4  4  6  2  2  4
31 | 4  8  2  10 2  2  2  2  6  0  0  2  2  4  10 8
32 | 4  2  6  4  4  2  2  4  6  6  4  8  2  2  8  0
33 | 4  4  6  2  10 8  4  2  4  0  2  2  4  6  2  4
34 | 0  8  16 6  2  0  0  12 6  0  0  0  0  8  0  6
35 | 2  2  4  0  8  0  0  0  14 4  6  8  0  2  14 0
36 | 2  6  2  2  8  0  2  2  4  2  6  8  6  4  10 0
37 | 2  2  12 4  2  4  4  10 4  4  2  6  0  2  2  4
38 | 0  6  2  2  2  0  2  2  4  6  4  4  4  6  10 10
39 | 6  2  2  4  12 6  4  8  4  0  2  4  2  4  4  0
3A | 6  4  6  4  6  8  0  6  2  2  6  2  2  6  4  0
3B | 2  6  4  0  0  2  4  6  4  6  8  6  4  4  6  2
3C | 0  10 4  0  12 0  4  2  6  0  4  12 4  4  2  0
3D | 0  8  6  2  2  6  0  8  4  4  0  4  0  12 4  4
3E | 4  8  2  2  2  4  4  14 4  2  0  2  0  8  4  4
3F | 4  8  4  2  4  0  2  4  4  2  4  8  8  6  2  2
"""
