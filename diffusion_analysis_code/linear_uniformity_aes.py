from lat_aes import *

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
    l = compute_lat(8, 8, -128, "aes")
    m, original_m = get_max_abs(l, 8, 8, 128)
    print("sbox", "aes", "linear uniformity", m, "original value", original_m)

    l = compute_lat(8, 8, -128, "inv")
    m, original_m = get_max_abs(l, 8, 8, 128)
    print("sbox", "inv", "linear uniformity", m, "original value", original_m)
