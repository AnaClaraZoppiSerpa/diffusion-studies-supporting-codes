"""
As S-Boxes do DES têm 6 bits na entrada e 4 bits na saída.

Então é algo assim:
f(x1, x2, x3, x4, x5, x6) = (y1, y2, y3, y4)
A entrada é um inteiro de 6 bits, cada bit é uma das variáveis booleanas.
A saída é um inteiro de 4 bits, cada bit é uma das coordenadas da função vetorial (f_i).
No entanto, tem aquela questão da indexação que o Jorge falou.
Na verdade as entradas são assim:
f(x1, x6, x2, x3, x4, x5).

Eu posso representar a minha função booleana desse jeito então.
Variáveis de entrada = um inteiro.
Saídas = um inteiro.
A função em si é um vetor.
Nesse caso especificamente, o vetor tem 2^6 posições, cujos valores vão no máximo até 2^4.

Montar a S-Box da figura desse jeito, e checar se ela está certa.

Exemplo de obtenção de ANF:

x1  x2  x3  f(x1, x2, x3)
0   0   0 -> 0
1   0   0 -> 1
0   1   0 -> 0
1   1   0 -> 0
0   0   1 -> 0
1   0   1 -> 1
0   1   1 -> 1
1   1   1 -> 1

a_v = somatório f(u), u no suporte de v
u << v se u_i <= v_i pra cada bit

Exemplos:
000 << 000
100 << 100, 000 << 100
010 << 010, 000 << 010
100 não << 010 por causa do primeiro bit (da esquerda pra direita)
"""

import sys

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

def get_anf_from_sbox_fi(which_sbox, which_fi):
    vs, fis = get_vs_and_fis_from_sbox(which_sbox, which_fi)
    poly = get_anf(vs, fis, 6)
    return poly

def anf_test():
    vs, fis = get_vs_and_fis_from_sbox(1, 1)
    print(get_anf(vs, fis, 6))

def get_vs_and_fis_from_sbox(which_sbox, which_fi):
    vs = []
    fis = {}
    for input_integer in range(2**6):
        sbox_output = get_sbox_result(which_sbox, input_integer)
        input_integer_binary = bin(input_integer)[2:].zfill(6)
        fis[input_integer_binary] = 0
        sbox_output_binary = bin(sbox_output)[2:].zfill(4)

        vs.append(input_integer_binary)
        fis[input_integer_binary] = int(sbox_output_binary[which_fi-1])

        #print(input_integer, "=", input_integer_binary, "->", sbox_output, "=", sbox_output_binary, "(fi = ", sbox_output_binary[which_fi-1] ,")")

    #print(vs)
    #print(fis)
    return vs, fis

def print_all_sbox_outputs(which_sbox):
    for i in range(2**6):
        res = get_sbox_result(which_sbox, i)
        i_binary = bin(i)[2:].zfill(6)
        res_binary = bin(res)[2:].zfill(4)
        print(i, "=", i_binary, "->", res, "=", res_binary)

def small_bin_test():
    i = int("110101", 2)
    print(bin(i)[2:])
    print(get_sbox_row(i), get_sbox_col(i))

def should_sum(u, v, n):
    for i in range(n):
        if u[i] > v[i]:
            return False

    return True

def turn_to_binary_vector(binary_string):
    vector = []
    for bit in binary_string:
        vector.append(int(bit))

    return vector

def get_term(binary_string):
    term = ""
    i = 1
    for bit in binary_string:
        if bit == "1":
            term += "x_"+str(i)
        i += 1

    if term == "":
        term = "1"

    return term

def get_des_term(binary_string):
    term = ""
    des_indexes = [1, 6, 2, 3, 4, 5]
    i = 0
    for bit in binary_string:
        if bit == "1":
            term += "x_"+str(des_indexes[i])
        i += 1

    if term == "":
        term = "1"

    return term

def get_poly(inputs, outputs):
    poly = ""
    for v in inputs:
        if outputs[v]:
            poly += get_term(v) + "+\n"

    poly
    return poly[:-1]

def get_as(vs, f, n):
    a = {}
    for v in vs:
        a[v] = 0
        for u in vs:
            if should_sum(u, v, n):
                a[v] ^= f[u]

    return a

def get_anf(vs, f, n):
    return get_poly(vs, get_as(vs, f, n))

def get_des_term_test():
    strs = ["000000", "010000", "000001", "000010"]
    for s in strs:
        print(s, get_des_term(s))

def small_get_anf_test_2():
    vs = ["00", "01", "10", "11"]
    f = {"00": 0, "01": 1, "11": 0, "10": 1}
    print(get_anf(vs, f, len(vs[0])))

def small_get_anf_test():
    vs = ["000", "100", "010", "110", "001", "101", "011", "111"]
    f = {"000": 0, "100": 1, "010": 0, "110": 0, "001": 0, "101": 1, "011": 1, "111": 1}
    print(get_anf(vs, f, len(vs[0])))

def small_get_term_test():
    vs = ["000", "100", "010", "110", "001", "101", "011", "111"]

    for v in vs:
        print(v, get_term(v))

def small_get_poly_test():
    vs = ["000", "100", "010", "110", "001", "101", "011", "111"]
    f = {"000": 0, "100": 1, "010": 0, "110": 0, "001": 0, "101": 1, "011": 1, "111": 1}

    a = get_as(vs, f, 3)

    print(get_poly(vs, a))

def small_get_as_test():
    vs = ["000", "100", "010", "110", "001", "101", "011", "111"]
    f = {"000": 0, "100": 1, "010": 0, "110": 0, "001": 0, "101": 1, "011": 1, "111": 1}

    a = get_as(vs, f, 3)

    for v in vs:
        print(v, a[v])

def small_should_sum_test():
    us = ["000", "001", "010", "011", "100", "101", "110", "111"]
    vs = ["000", "001", "010", "011", "100", "101", "110", "111"]
    wished_sums = {}

    for v in vs:
        wished_sums[v] = []

    for u in us:
        for v in vs:
            if should_sum(u, v, 3):
                wished_sums[v].append(u)

    for v in vs:
        print(v)
        print(wished_sums[v])

def monomial_count(anf_string):
    mons = anf_string.split()
    print("Há", len(mons), "monômios")
    max = 0
    mon = ""
    for s in mons:
        if len(s) > max:
            max = len(s)
            mon = s
    print("Maior monômio:", mon)

symbol = 'x_'
for s in [1, 2, 3, 4, 5, 6, 7, 8]:
    for y in [1, 2, 3, 4]:
        print("Encontrando ANF de y", y, "da S-Box", s, "do DES:")
        anf_string = get_anf_from_sbox_fi(s, y)
        #print(anf_string)
        monomial_count(anf_string)
