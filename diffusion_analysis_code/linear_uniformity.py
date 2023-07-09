from lat import *

def get_max_abs(lat, input_size, output_size, ignore):
    max = 0
    real_max = 0
    for mask_a in range(1, 2**input_size): # input mask
        for mask_b in range(1, 2**output_size): # output mask
            if abs(lat[mask_a-1][mask_b-1]) != ignore and abs(lat[mask_a-1][mask_b-1]) > max:
                max = abs(lat[mask_a-1][mask_b-1])
                real_max = lat[mask_a-1][mask_b-1]
    return max, real_max

if __name__ == "__main__":
    for sbox in range(1, 9):
        l = compute_lat(6, 4, -32, sbox)
        m, original_m = get_max_abs(l, 6, 4, 32)
        print("sbox", sbox, "linear uniformity", m, "original value", original_m)
