order = 8
shark_poly = 0x1f5
# Binary representation: 111110101
# Equivalent poly: 1x^8 + 1x^7 + 1x^6 + 1x^5 + 1x^4 + 0x^3 + 1x^2 + 0x^1 + 1x^0
# x^8 + x^7 + x^6 + x^5 + x^4 + x^2 + 1
degree_limit_mask = 0b100000000 # 0x100 = 100000000 (binary)

# Adicionar outros polinômios
# square_poly
# bksq_poly
# rijndael_poly
# khazad_poly
# anubis_poly
# e por aí vai

alog = [0 for i in range(2**order)]
log = [0 for i in range(2**order)]

irreducible_poly = shark_poly

def init_discrete_log_tables():
    alog[0] = 1
    for i in range(1, 2**order):
        j = alog[i-1] << 1
        if j & degree_limit_mask:
            j = j ^ irreducible_poly
        alog[i] = j
    log[0] = 0
    for i in range(1, 2**order - 1):
        log[alog[i]] = i

def add(poly1, poly2):
    return poly1 ^ poly2

def subtract(poly1, poly2):
    return poly1 ^ poly2

def multiply(poly1, poly2):
    if poly1 == 0:
        return 0
    if poly2 == 0:
        return 0
    
    modulus = 2**order - 1
    return alog[(log[poly1] + log[poly2]) % modulus]

def invert(poly):
    if poly == 0:
        return 0
    
    modulus = 2**order - 1
    return alog[-log[poly] + modulus]

def matrix_multiplication(A, B, dim):
    for i in range(0, dim):
        for j in range(0, dim):
            
    pass

def matrix_determinant(A, dim):
    pass

def matrix_inversion(A, dim):
    pass



