from sbox_aux import *

def compute_linear_expression(x, mask, bits):
    xor = 0
    for s in range(bits):
        x_s = (x >> s) & 1
        mask_s = (mask >> s) & 1
        and_result = x_s & mask_s
        xor = xor ^ and_result
    return xor

def compute_lat(input_size, output_size, initial_value, sbox):
    lat = [ [initial_value for i in range(1, 2**output_size)] for j in range(1, 2**input_size) ]

    #for mask_a in range(2**input_size): # input mask
    #    lat[mask_a] = {}
    #    for mask_b in range(2**output_size): # output mask
    #        lat[mask_a][mask_b] = initial_value

    for mask_a in range(1, 2**input_size): # input mask
        for mask_b in range(1, 2**output_size): # output mask
            for x in range(2**input_size): # input
                left_side = compute_linear_expression(x, mask_a, input_size)
                right_side = compute_linear_expression(get_sbox_result(sbox, x), mask_b, output_size)
                if left_side == right_side:
                    lat[mask_a-1][mask_b-1] += 1
    return lat

def print_lat(lat, input_size, output_size):
    for mask_a in range(1, 2**input_size): # input mask
        for mask_b in range(1, 2**output_size): # output mask
            print("a =", mask_a, "b =", mask_b, "->", lat[mask_a-1][mask_b-1])

def pandas_lat(lat):
    A = np.array(lat)
    df_cols = []
    for i in range(1, 2**4):
        df_cols.append(str(i))

    df = pd.DataFrame(A, columns=df_cols)
    df.index += 1
    pd.set_option('display.max_rows', None)
    print(df)
    #df.to_csv("LAT/no_zero_index_sbox"+sys.argv[1]+".csv")

def do_it():
    l = compute_lat(6, 4, -32, int(sys.argv[1]))
    #print_lat(l, 6, 4)
    pandas_lat(l)

if __name__ == "__main__":
    do_it()
