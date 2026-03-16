import sys
import math

r = float(sys.stdin.readline())
x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())

def dist(xa, ya, xb, yb):
    return math.hypot(xa - xb, ya - yb)

direct = dist(x1, y1, x2, y2)

dx = x2 - x1
dy = y2 - y1
a = dx * dx + dy * dy
b = 2 * (x1 * dx + y1 * dy)
c = x1 * x1 + y1 * y1 - r * r

discriminant = b * b - 4 * a * c

if discriminant <= 0:
    print(f"{direct:.10f}")
else:
    d1 = math.hypot(x1, y1)
    d2 = math.hypot(x2, y2)

    if d1 <= r or d2 <= r:
        print(f"{direct:.10f}")
    else:
        cos_theta = (x1 * x2 + y1 * y2) / (d1 * d2)
        cos_theta = max(-1.0, min(1.0, cos_theta))
        theta = math.acos(cos_theta)

        alpha = math.acos(r / d1)
        beta = math.acos(r / d2)

        arc_angle = theta - alpha - beta
        if arc_angle < 0:
            print(f"{direct:.10f}")
        else:
            arc = r * arc_angle
            tangent1 = math.sqrt(d1 * d1 - r * r)
            tangent2 = math.sqrt(d2 * d2 - r * r)
            result = tangent1 + tangent2 + arc
            print(f"{result:.10f}")