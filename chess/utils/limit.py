def limit(low, val, high):
    if val < low:
        return low
    elif val > high:
        return high
    return val