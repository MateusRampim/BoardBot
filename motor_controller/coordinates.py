import math

def polar_to_cartesian(r0, r1, w, h):
    x = (r0**2 - r1**2 + w**2) / (2*w)
    y = math.sqrt(r0**2 - x**2)
    return (x, y)

def cartesian_to_polar(x, y, w, h):
    r0 = math.sqrt(x**2 + y**2)
    r1 = math.sqrt((w-x)**2 + y**2)

    return (r0, r1)
