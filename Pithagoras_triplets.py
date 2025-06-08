# 1-15

for side_a in range(1,16):
    for side_b in range(side_a + 1, 16):
        for side_c in range(side_b + 1, 16):
            if side_a**2 + side_b**2 == side_c **2:
                print(side_a, side_b, side_c)
