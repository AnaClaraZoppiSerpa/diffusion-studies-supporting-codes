import sys
safer_sbox = [
    1,45,226,147,190,69,21,174,120,3,135,164,184,56,207,63,8,103,9,148,235,38,168,107,189,24,52,27,187,191,114,247,64,53,72,156,81,47,59,85,227,192,159,216,211,243,141,177,255,167,62,220,134,119,215,166,17,251,244,186,146,145,100,131,241,51,239,218,44,181,178,43,136,209,153,203,140,132,29,20,129,151,113,202,95,163,139,87,60,130,196,82,92,28,232,160,4,180,133,74,246,19,84,182,223,12,26,142,222,224,57,252,32,155,36,78,169,152,158,171,242,96,208,108,234,250,199,217,0,212,31,110,67,188,236,83,137,254,122,93,73,201,50,194,249,154,248,109,22,219,89,150,68,233,205,230,70,66,143,10,193,204,185,101,176,210,198,172,30,65,98,41,46,14,116,80,2,90,195,37,123,138,42,91,240,6,13,71,111,112,157,126,16,206,18,39,213,76,79,214,121,48,104,54,117,125,228,237,128,106,144,55,162,94,118,170,197,127,61,175,165,229,25,97,253,77,124,183,11,238,173,75,34,245,231,115,35,33,200,5,225,102,221,179,88,105,99,86,15,161,49,149,23,7,58,40
]

safer_inv_sbox = [0 for i in range(256)]
for i in range(256):
    sbox_value = safer_sbox[i]
    safer_inv_sbox[sbox_value] = i

def get_sbox_result(which_sbox, input_int):
    if which_sbox == 'inv':
        return safer_inv_sbox[input_int]
    if which_sbox == '':
        return safer_sbox[input_int]

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

def term_count(anf_string):
    for i in range(1, 9):
        print(symbol+str(i), 'aparece', anf_string.count(symbol+str(i)), 'vezes')

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
    print(symbol+'1 aparece?', symbol+'1' in anf_string)
    print(symbol+'2 aparece?', symbol+'2' in anf_string)
    print(symbol+'3 aparece?', symbol+'3' in anf_string)
    print(symbol+'4 aparece?', symbol+'4' in anf_string)
    print(symbol+'5 aparece?', symbol+'5' in anf_string)
    print(symbol+'6 aparece?', symbol+'6' in anf_string)
    print(symbol+'7 aparece?', symbol+'7' in anf_string)
    print(symbol+'8 aparece?', symbol+'8' in anf_string)
    term_count(anf_string)

output_bit = int(sys.argv[1])

symbol = 'x_'
print("Encontrando ANF de y", output_bit, "da S-Box", '', "do SAFER:")
sbox_anf = get_anf_from_sbox_fi('', output_bit)
print(sbox_anf)
#validation(sbox_anf)
#monomial_count(sbox_anf)

symbol = 'y_'
print("Encontrando ANF de x", output_bit, "da S-Box", 'inv', "do SAFER:")
inv_anf = get_anf_from_sbox_fi('inv', output_bit)
print(inv_anf)
#validation(inv_anf)
#monomial_count(inv_anf)
