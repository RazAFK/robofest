def constrain(x, start, end):
    if x<=start: return start
    if end<=x: return end
    return x