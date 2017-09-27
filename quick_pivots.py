def calc_pivots(h,l,c):
    def calculate_pivots(high, low, close):
        H, L, C = [float(high), float(low), float(close)]
        PP = float(H + L + C) / 3
        R1 = (2 * PP) - L
        S1 = (2 * PP) - H
        R2 = (PP - S1) + R1
        S2 = PP - (R1 - S1)
        R3 = (PP - S2) + R2
        S3 = PP - (R2 - S2)
        return {
            'r': [
                R1, R2, R3
            ],
            's': [
                S3, S2, S1
            ],
            'pp': PP
        }
    return calculate_pivots(h,l,c)
