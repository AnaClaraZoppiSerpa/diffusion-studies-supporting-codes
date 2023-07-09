prime_p = 2
order_m = 8
irreducible_poly = [1, 1, 0, 1, 1, 0, 0, 0, 1] #x^8 + x^4 + x^3 + x + 1

def int_matrix_determinant(A):
    n = len(A)
    AM = copy_matrix(A)
 
    for fd in range(n):
        for i in range(fd+1,n):
            if AM[fd][fd] == 0:
                AM[fd][fd] == 1.0e-18
            crScaler = AM[i][fd] / AM[fd][fd] 
            for j in range(n): 
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
     
    product = 1.0
    for i in range(n):
        product *= AM[i][i] 
 
    return product

def matrix_determinant(matrix, dimension):
    copy = 

def is_valid_poly(poly):
    assert(len(poly) == order_m)
    for coefficient in poly:
        assert(coefficient >= 0 and coefficient < prime_p)
    
    return True

def multiplicative_inverse(poly):
    pass

def add_two_elements(poly1, poly2):
    assert(is_valid_poly(poly1))
    assert(is_valid_poly(poly2))
    
    result = []
    for i in range(order_m):
        result.append(coefficient_addition(poly1[i], poly2[i]))
    
    assert(is_valid_poly(result))
    return result

def coefficient_addition(coeff1, coeff2):
    assert(coeff1 < prime_p)
    assert(coeff2 < prime_p)
    return (coeff1 + coeff2) % prime_p

def multiply_two_elements(poly1, poly2):
    pass

poly1 = [1, 1, 0, 1, 1, 0, 0, 0]
poly2 = [1, 1, 1, 1, 1, 0, 1, 0]
print(add_two_elements(poly1, poly2))


