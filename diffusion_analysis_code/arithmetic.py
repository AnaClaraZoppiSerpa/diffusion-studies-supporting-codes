# Parameters:
# - Modulus regarding polynomial coefficients (e.g 2 for AES)
# - Maximum degree of the polynomials (e.g 7 for AES)
# - Polynomial for modular reduction when multiplying

# Polynomial = array
# Position 0 = coefficient for degree 0
# Position 1 = coefficient for degree 1
# Position N = coefficient for degree N

# Adição de coeficientes
# Adição de 2 polinômios
# Multiplicação de 2 polinômios
# Redução pelo outro polinômio lá

# Quando os polinômios são binários, coeficientes são 1 ou 0.
# Adicionar os coeficientes módulo 2 é equivalente a fazer o XOR.
# Então dá pra representar como um inteiro de N bits, sendo N-1 o grau, e fazer XOR bit a bit.
def add_binary_polynomials(p, q):
    return p ^ q

def int_to_poly_str(p):
    degree = 0
    coeff = 0
    poly = p
    terms = []
    while poly != 0:
        coeff = poly & 1
        if coeff != 0:
            if degree == 0:
                terms.append(str(coeff))
            else:
                terms.append('x^'+str(degree))
        poly >>= 1
        degree += 1

    return terms

def modular_addition(a, b, modulus):
    return (a + b) % modulus

def add_polynomials(p, q, modulus):
    degree_p = len(p) - 1
    degree_q = len(q) - 1
    result = []
    for i in range(max(degree_p, degree_q)+1):
        p_coeff = 0
        q_coeff = 0
        if i <= degree_p:
            p_coeff = p[i]
        if i <= degree_q:
            q_coeff = q[i]

        result.append(modular_addition(p_coeff, q_coeff, modulus))
    return result

def multiply_polynomials(poly1, poly2, mod_poly, mod_coeff):
    pass

def generic_poly_str(p):
    degree = 0
    coeff = 0
    terms = []
    while degree <= len(p) - 1:
        coeff = p[degree]
        if coeff != 0:
            if degree == 0:
                terms.append(str(coeff))
            else:
                if coeff != 1:
                    terms.append(str(coeff)+'x^'+str(degree))
                else:
                    terms.append('x^'+str(degree))
        degree += 1

    return terms

def test():
    print(int_to_poly_str(255))
    print(generic_poly_str([3, 4, 10, 0, 0, 0, 7, 29]))

test()
