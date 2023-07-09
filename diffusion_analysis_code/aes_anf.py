import sys
from aes_sbox_aux import *

# Bits de entrada: de 1 até 8
# Bits de saída: de 1 até 8

def get_sbox_result(which_sbox, input_int):
    if which_sbox == 'inv':
        return aes_inv_sbox[input_int]
    if which_sbox == '':
        return aes_sbox[input_int]

def get_anf_from_sbox_fi(which_sbox, which_fi):
    vs, fis = get_vs_and_fis_from_sbox(which_sbox, which_fi)
    poly = get_anf(vs, fis, 8)
    return poly

def get_term(binary_string):
    term = ""
    i = 1
    for bit in binary_string:
        if bit == "1":
            term += symbol+str(i)
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

def should_sum(u, v, n):
    for i in range(n):
        if u[i] > v[i]:
            return False

    return True

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

def get_vs_and_fis_from_sbox(which_sbox, which_fi):
    vs = []
    fis = {}
    for input_integer in range(2**8):
        sbox_output = get_sbox_result(which_sbox, input_integer)
        input_integer_binary = bin(input_integer)[2:].zfill(8)
        fis[input_integer_binary] = 0
        sbox_output_binary = bin(sbox_output)[2:].zfill(8)

        vs.append(input_integer_binary)
        fis[input_integer_binary] = int(sbox_output_binary[which_fi-1])

    return vs, fis

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

def validation(anf_string):
    # Difusão completa
    assert(symbol+'1' in anf_string)
    assert(symbol+'2' in anf_string)
    assert(symbol+'3' in anf_string)
    assert(symbol+'4' in anf_string)
    assert(symbol+'5' in anf_string)
    assert(symbol+'6' in anf_string)
    assert(symbol+'7' in anf_string)
    assert(symbol+'8' in anf_string)
    print("Todos os termos aparecem!")
    # Tabela verdade?

output_bit = int(sys.argv[1])

symbol = "x_"
print("Encontrando ANF de y", output_bit, "da S-Box", '', "do AES:")
sbox_anf = get_anf_from_sbox_fi('', output_bit)
#print(sbox_anf)
#validation(sbox_anf)
monomial_count(sbox_anf)

symbol = "y_"
print("Encontrando ANF de x", output_bit, "da S-Box", 'inv', "do AES:")
inv_anf = get_anf_from_sbox_fi('inv', output_bit)
#print(inv_anf)
#validation(inv_anf)
monomial_count(inv_anf)
